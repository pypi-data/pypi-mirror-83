import click
import uuid
import json
import requests
import subprocess
import random
import time

from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
)
from spell.cli.utils import cluster_utils, sentry

DEFAULT_REGION = "westus2"
CONTAINER_NAME = "spell-blob-container"
VNET_NAME = "spell-vnet"
SUBNET_NAME = "spell-subnet"
SECURITY_GROUP_NAME = "spell-security-group"
NUM_RETRIES = 5  # Retries for getting sp/app
# SSH, Docker Daemon, and Jupyter respectively
INGRESS_PORTS = [22, 2376, 9999]

required_permissions = [
    "Microsoft.Compute/*",
    "Microsoft.Network/*",
    "Microsoft.Storage/*",
    "Microsoft.Support/*",
    "Microsoft.Authorization/*/read",
    "Microsoft.Resources/deployments/*",
    "Microsoft.Resources/subscriptions/resourceGroups/read",
]


@click.command(name="az", short_help="Sets up an Azure VNet as a Spell cluster", hidden=True)
@click.pass_context
@click.option(
    "-n", "--name", "name", help="This will be used by Spell for you to identify the cluster"
)
@click.option(
    "-r",
    "--resource-group",
    "resource_group_name",
    help="This will be the name of the Resource Group Spell will create and "
    "store all its resources in within your Azure account",
    default="spell-resource-group",
)
@click.option(
    "-s",
    "--service-principal",
    "service_principal_name",
    help="Command to name your Service Principal",
    default="spell-sp",
)
def create_azure(ctx, name, resource_group_name, service_principal_name):
    """
    This command creates an Azure VNet of your choosing as an external Spell cluster.
    This will let your organization create runs in that VNet, so your data never leaves
    your VNet. You create an Azure Blob Container of your choosing for all run outputs to be written to.
    After this cluster is set up you will be able to select the types and number of machines
    you would like Spell to create in this cluster.
    """

    # Verify the owner is the admin of an org
    spell_client = ctx.obj["client"]
    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])

    try:
        from azure.graphrbac import GraphRbacManagementClient
        from azure.mgmt.resource import ResourceManagementClient
        from azure.mgmt.authorization import AuthorizationManagementClient
        from azure.mgmt.resource.subscriptions import SubscriptionClient
        from azure.mgmt.storage import StorageManagementClient
        from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku, SkuName, Kind
        from spell.cli.utils.azure_credential_wrapper import AzureIdentityCredentialAdapter
        from azure.core.exceptions import ClientAuthenticationError
        from azure.storage.blob import BlobServiceClient
        from azure.mgmt.network import NetworkManagementClient
        from azure.identity import DefaultAzureCredential

    except ImportError:
        click.echo("Please `pip install --upgrade 'spell[cluster-azure]'` and rerun this command")
        return

    click.echo(
        """This command will help you
        - Select a region to create resources in and a subscription for billing
        - Create an App and Service Principal
        - Create a Resource group in the specified region to manage your resources
        - Assign a role to your Service Principal that allows Spell to spin up and
            down machines and access your Blobs
        - Create a uniquely-named storage account
        - Set up an Blob Container to store your run outputs in
        - Set up a VNet and Subnet which Spell will spin up workers in to run your jobs
        - Set up a Security Group providing Spell SSH and Docker access to workers """
    )

    # Create Credentials
    """
    DefaultAzureCredential is the new credential that Microsoft recommends. However,
    this credential only works for packages with the prefix `azure-mgmt`.
    The hope is that eventually everything will use this credential. Until that happens,
    they recommend using the wrapper AzureIdentityCredentialAdapter().

    The resource id argument supplied to the wrapper dictates which token is returned. Different
    APIs require different tokens.

    credentials (Default Azure Credential): Azure's new credential that uses the azure identity
    library.
    management_creds (wrapper/default resource id): used for tenant id and authorization client
    graph_rbac_creds (wrapper/graph.windows.net resource id): used to create app/sp - library is
    being deprecated and will eventually use the following credential
    microsoft_graph_creds (wrapper/graph.microsoft.com resource id): This uses the new Microsoft
    Graph API to set client secret.

    https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate?tabs=cmd
    """
    # TODO(sruthi): Figure out a better way to authenticate
    try:
        credentials = DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True,
            exclude_visual_studio_code_credential=True,
            exclude_shared_token_cache_credential=True,
        )
        management_cred = AzureIdentityCredentialAdapter()
        management_cred.set_token()
        graph_rbac_creds = AzureIdentityCredentialAdapter(resource_id="https://graph.windows.net/")
        graph_rbac_creds.set_token()
        microsoft_graph_creds = AzureIdentityCredentialAdapter(
            resource_id="https://graph.microsoft.com/"
        )
        microsoft_graph_creds.set_token()
    except ClientAuthenticationError:
        # NOTE: Default Azure Credential raises its own error
        raise ExitException("Please try again after logging into azure in your terminal")

    # Validate cluster name
    cluster_utils.echo_delimiter()
    if not name:
        name = click.prompt("Enter a display name for this Azure cluster within Spell")

    with api_client_exception_handler():
        spell_client.validate_cluster_name(name)

    # Queries for Subscription Id
    subscription_client = SubscriptionClient(credentials)
    subscription_id = get_subscription(subscription_client)
    if subscription_id is None:
        raise ExitException("No active subscriptions found")
    tenant_id = get_tenant_id(name)

    # Get Region
    available_regions = [
        location.name
        for location in subscription_client.subscriptions.list_locations(subscription_id)
    ]
    cluster_utils.echo_delimiter()
    region = click.prompt(
        "Please choose a region for your cluster. This might affect machine availability",
        type=click.Choice(available_regions),
        default=DEFAULT_REGION,
    )
    supports_no_gpu = region in (
        "canadaeast",
        "centralus",
        "westcentralus",
        "southafricawest",
        "eastasia",
        "australiacentral",
        "australiacentral2",
        "australiasoutheast",
        "brazilsoutheast",
        "chinaeast",
        "chinanorth",
        "francesouth",
        "germany",
        "germanycentral",
        "germanynorth",
        "germanywestcentral",
        "southindia",
        "westindia",
        "japanwest",
        "koreasouth",
        "switzerlandnorth",
        "switzerlandwest",
        "uaecentral",
        "ukwest",
    )
    if supports_no_gpu:
        if not click.confirm(
            "Azure does not support GPU types in {}. You can still create a cluster, but it will "
            "only have access to CPU types - continue?".format(region)
        ):
            return

    # Create Service Principal
    client = GraphRbacManagementClient(graph_rbac_creds, tenant_id)
    client_id, sp_object_id, app_object_id = create_service_principal(
        client, service_principal_name, name
    )
    client_secret, client_secret_expiration_date = set_client_secret(
        microsoft_graph_creds, sp_object_id
    )

    # Create Resource Group
    resource_client = ResourceManagementClient(credentials, subscription_id)
    if resource_client.resource_groups.check_existence(resource_group_name):
        raise ExitException(
            "Resource group `{}` already exists - "
            "please select a different name".format(resource_group_name)
        )
    resource_group = resource_client.resource_groups.create_or_update(
        resource_group_name, {"location": region}
    )

    # Creates and Assigns Custom Role to Service Principal
    authorization_client = AuthorizationManagementClient(management_cred, subscription_id)
    create_and_assign_role(
        management_cred,
        subscription_id,
        authorization_client,
        resource_group.id,
        sp_object_id,
        resource_group_name,
    )

    # Create Networking
    network_client = NetworkManagementClient(credentials, subscription_id)
    create_network(network_client, resource_group_name, region)

    # Creates Storage Account
    storage_client = StorageManagementClient(credentials, subscription_id)
    params = StorageAccountCreateParameters(
        sku=Sku(name=SkuName.standard_ragrs), kind=Kind.storage, location=region,
    )
    storage_account, storage_account_name = create_storage_account(
        storage_client, name, resource_group_name, params
    )

    # Get Storage Key
    list_keys = storage_client.storage_accounts.list_keys(resource_group_name, storage_account_name)
    storage_keys = {v.key_name: v.value for v in list_keys.keys}
    storage_key = storage_keys["key1"]

    # Creates Blob Container
    blob_service_client = BlobServiceClient(
        account_url=storage_account.primary_endpoints.blob, credential=storage_key
    )
    create_blob_container(storage_account_name, blob_service_client)

    with api_client_exception_handler():
        cluster = spell_client.create_azure_cluster(
            name,
            app_object_id,
            client_id,
            client_secret,
            client_secret_expiration_date,
            region,
            resource_group_name,
            sp_object_id,
            storage_account_name,
            subscription_id,
            tenant_id,
        )
        cluster_utils.echo_delimiter()
        url = "{}/{}/clusters/{}".format(ctx.obj["web_url"], ctx.obj["owner"], cluster["name"])
        click.echo(
            "Your cluster {} is initialized! Head over to the web console to create machine types "
            "to execute your runs on - {}".format(name, url)
        )


def get_tenant_id(name):
    """
    Shells out to Azure CLI to get Tenant ID
    """
    try:
        process = subprocess.run(
            ["az", "account", "show"], check=True, stdout=subprocess.PIPE, universal_newlines=True
        )
        output = process.stdout
        data = json.loads(output)
        tenant_id = data["tenantId"]
    except Exception as e:
        # TODO(sruthi): Remove for customer when we are finished developing
        click.echo("ERROR: While extracting tenant id. Error was: {}".format(e), err=True)
        sentry.capture_message(
            "Error occured when extracting tenant id using the Azure CLI for cluster {}: "
            "Error was '{}''".format(name, e)
        )
        tenant_id = click.prompt("Enter tenant id of Azure Active Directory")
    return tenant_id


def get_subscription(client):
    sub_ids = [sub.subscription_id for sub in client.subscriptions.list() if sub.state == "Enabled"]
    if not sub_ids:
        return None
    elif len(sub_ids) == 1:
        click.echo(
            "One Subscription found: {}. "
            "Defaulting to this subscription for this cluster".format(sub_ids[0])
        )
        return sub_ids[0]
    else:
        cluster_utils.echo_delimiter()
        return click.prompt(
            "Please choose a subscription id from your active subscriptions",
            type=click.Choice(sub_ids),
        )


def create_service_principal(client, service_principal_name, name):
    """
    Creates an App `spell-sp` and Service Principal
    Returns the client id aka. appID and object id of the sp
    TODO(sruthi): Switch to use Microsoft Graph REST API instead of deprecated AD Graph API
    """
    from azure.graphrbac.models.graph_error import GraphErrorException

    cluster_utils.echo_delimiter()
    click.echo("Creating Service Principal")
    try:
        app = client.applications.create(
            {"available_to_other_tenants": False, "display_name": service_principal_name}
        )
        sp = client.service_principals.create({"app_id": app.app_id, "account_enabled": True})
    except GraphErrorException as e:
        sentry.capture_message(
            "Error occured when attempting to create service principal for cluster {}: "
            "Error was '{}''".format(name, e)
        )
        raise ExitException(
            "Please ensure that your user has the appropriate Azure Active Directory Admin Role "
            "needed to create service principals in your local tenant."
        )

    # Waits for App and Service Principal to be created
    for i in range(NUM_RETRIES):
        try:
            client.applications.get(app.object_id)
            client.service_principals.get(sp.object_id)
        except GraphErrorException as e:
            is_app_exception = "Resource '{}' does not exist".format(app.object_id) in str(e)
            is_sp_exception = "Resource '{}' does not exist".format(sp.object_id) in str(e)
            if not is_app_exception and not is_sp_exception:
                sentry.capture_exception(e)
                raise ExitException(
                    "Was not able to read newly created Service Principal `{}`".format(
                        service_principal_name
                    )
                )
            if i == NUM_RETRIES - 1:
                sentry.capture_message(
                    "Retried {} times to get service principal `{}` for cluster `{}`. Error was '{}'".format(
                        NUM_RETRIES, service_principal_name, name, e
                    )
                )
                raise ExitException(
                    "Was not able to Get Service Principal `{}`".format(service_principal_name)
                )
            time.sleep(3)
        else:
            break
    click.echo("Service Principal `{}` Created!".format(service_principal_name))
    return app.app_id, sp.object_id, app.object_id


def set_client_secret(credentials, object_id):
    """
    Uses Microsoft Graph REST API to generate a client secret
    Returns the client secret and the end date (date the client secret expires)

    NOTE: There is no Python client library for this, so we do raw HTTP requests to the API.
    In the future we will use the python client API that has not yet been released.
    """

    # Create Request
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(credentials.token["access_token"]),
    }
    url = "https://graph.microsoft.com/v1.0/servicePrincipals/{}/addPassword".format(object_id)
    payload = {
        "passwordCredential": {"displayName": "spellClientSecret"},
    }
    # POST request
    try:
        response = requests.post(url, data=json.dumps(payload), headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ExitException("Error setting client secret: {}".format(e.response.text))

    # Return Client Secret and Expiration Date
    secret_info = json.loads(response.text)
    return secret_info["secretText"], secret_info["endDateTime"]


def create_and_assign_role(
    credentials, subscription_id, authorization_client, group_id, object_id, resource_group_name
):
    """Creates a custom `Spell-Access` role with the specified permissions """

    role_definition_id = str(uuid.uuid4())
    role_name = "SpellAccess_{}".format(str(random.randint(10 ** 6, 10 ** 7)))
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(credentials.token["access_token"]),
    }
    scope = "subscriptions/{}/resourceGroups/{}".format(subscription_id, resource_group_name)
    url = (
        "https://management.azure.com/{}/providers/Microsoft.Authorization/"
        "roleDefinitions/{}?api-version=2015-07-01".format(scope, role_definition_id)
    )
    payload = {
        "name": role_definition_id,
        "properties": {
            "roleName": role_name,
            "description": "Spell Access Role to let Spell spin up and down worker machines and access your blobs",
            "type": "CustomRole",
            "permissions": [{"actions": required_permissions}],
            "assignableScopes": [scope],
        },
    }
    cluster_utils.echo_delimiter()
    click.echo(
        "Creating role {} with the following permissions: \n{} \n...".format(
            role_name, "\n".join("\t" + p for p in required_permissions)
        )
    )
    try:
        response = requests.put(url, data=json.dumps(payload), headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ExitException("Error creating role: {}".format(e.response.text))

    click.echo("Role Created!")

    roles = list(
        authorization_client.role_definitions.list(
            group_id, filter="roleName eq '{}'".format(role_name)
        )
    )
    assert len(roles) == 1, (
        "Found unexpected number of roles ({}) with name {}. "
        "Expected exactly 1".format(len(roles), role_name)
    )
    spell_role = roles[0]

    # Assign Custom Role to Service Principal
    authorization_client.role_assignments.create(
        group_id,
        uuid.uuid4(),
        {
            "role_definition_id": spell_role.id,
            "principal_id": object_id,
            "principal_type": "ServicePrincipal",
        },
    )


def create_network(network_client, resource_group_name, region):
    from azure.mgmt.network.v2020_06_01.models import SecurityRule
    from azure.mgmt.network.v2020_06_01.models import NetworkSecurityGroup
    from azure.core.exceptions import HttpResponseError

    cluster_utils.echo_delimiter()
    click.echo("Creating VNet")

    # Create VPC
    cidr = u"10.0.0.0/16"
    async_vnet_creation = network_client.virtual_networks.begin_create_or_update(
        resource_group_name,
        VNET_NAME,
        {"location": region, "address_space": {"address_prefixes": [cidr]}},
    )
    async_vnet_creation.wait()

    # Create Subnet
    async_subnet_creation = network_client.subnets.begin_create_or_update(
        resource_group_name, VNET_NAME, SUBNET_NAME, {"address_prefix": cidr}
    )
    async_subnet_creation.result()

    # Create Security Group
    nsg_params = NetworkSecurityGroup(
        id=SECURITY_GROUP_NAME, location=region, tags={"name": VNET_NAME}
    )
    try:
        nsg = network_client.network_security_groups.begin_create_or_update(
            resource_group_name, SECURITY_GROUP_NAME, parameters=nsg_params
        )
    except HttpResponseError as e:
        raise ExitException("Unable to create new security group. Azure error: {}".format(e))

    # Add Outbound Security Rules for Ingress Ports
    priority = 100  # Determines the order in which Security Rules get processed, lower numbers have higher priority
    for port in INGRESS_PORTS:
        security_rule_name = "spell-security-rule-{}".format(port)
        security_rule_parameters = SecurityRule(
            name=security_rule_name,
            description="Allows the Spell API SSH and Docker access to worker machines",
            protocol="Tcp",
            source_port_range="*",
            destination_port_range=port,
            source_address_prefix="*",
            destination_address_prefix="*",
            access="Allow",
            direction="Inbound",
            priority=priority,
        )
        try:
            network_client.security_rules.begin_create_or_update(
                resource_group_name,
                SECURITY_GROUP_NAME,
                security_rule_name,
                security_rule_parameters,
            )
        except HttpResponseError as e:
            raise ExitException("Error creating Security Rule. Azure error: {}".format(e))
        priority += 1

    click.echo("Successfully created Security Group `{}`".format(nsg.result().name))


def create_storage_account(storage_client, cluster_name, resource_group_name, params):
    from azure.core.exceptions import HttpResponseError
    from azure.mgmt.storage.v2019_06_01.models import StorageAccountCheckNameAvailabilityParameters

    """Creates a Storage Account and returns Storage Client, Storage Account"""

    cluster_utils.echo_delimiter()

    default_name = "".join(filter(str.isalnum, "spell{}storage".format(cluster_name[:13]).lower()))
    storage_account_name = click.prompt(
        "Please enter a name for the Azure Storage Account Spell will create to store run outputs.\n"
        "NOTE: Storage account names must be between 3 and 24 characters in length and may only contain "
        "numbers and lowercase letters.\nYour storage account name must be UNIQUE within Azure. "
        "No two storage accounts can have the same name.",
        default=default_name,
    ).strip()
    account_name = StorageAccountCheckNameAvailabilityParameters(name=storage_account_name)
    # Built in Azure Storage Account name validator
    availability = storage_client.storage_accounts.check_name_availability(account_name)
    if not availability.name_available:
        click.echo(
            "Azure does not support this name for the following reason: {}".format(
                availability.reason
            )
        )
        return create_storage_account(storage_client, cluster_name, resource_group_name, params)

    # Create Storage Account
    try:
        storage_async_operation = storage_client.storage_accounts.begin_create(
            resource_group_name, storage_account_name, params,
        )
        storage_account = storage_async_operation.result()
    except HttpResponseError as e:
        click.echo("Unable to create storage account. Azure error: {}".format(e), err=True)
        return create_storage_account(storage_client, cluster_name, resource_group_name, params)

    click.echo(
        "Storage account `{}` under resource group `{}` created!".format(
            storage_account_name, resource_group_name
        )
    )
    return storage_account, storage_account_name


def create_blob_container(storage_account_name, blob_service_client):
    """Creates a Blob Container and returns the Container Client"""

    cluster_utils.echo_delimiter()

    for i in range(3):
        try:
            blob_service_client.create_container(storage_account_name)
            click.echo("Created your new blob container `spell-blob-container`!")
            return
        except Exception as e:
            click.echo("Unable to create blob container. Azure error: {}".format(e), err=True)

    raise ExitException("Could not create blob container after three retries.")


def delete_azure_cluster(ctx, cluster):
    """
    Deletes an Azure cluster, including the Spell Cluster, Machine Types,
    Security Principal, Resource Group, Vnet, Storage Accounts, and Roles associated with this cluster.
    """

    spell_client = ctx.obj["client"]
    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])

    try:
        from azure.graphrbac import GraphRbacManagementClient
        from azure.mgmt.resource import ResourceManagementClient
        from spell.cli.utils.azure_credential_wrapper import AzureIdentityCredentialAdapter
        from azure.core.exceptions import ClientAuthenticationError
        from azure.identity import DefaultAzureCredential

    except ImportError:
        click.echo("Please `pip install --upgrade 'spell[cluster-azure]'` and rerun this command")
        return

    click.echo(
        "This command will delete the Spell Cluster, Machine Types, Service Principal, "
        "VNet, Custom Role, Resource Group, and Storage Account associated with this cluster. "
    )
    if not click.confirm(
        "Are you SURE you want to delete the spell cluster {}?".format(cluster["name"])
    ):
        return
    # Create Credentials
    try:
        credentials = DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True,
            exclude_visual_studio_code_credential=True,
            exclude_shared_token_cache_credential=True,
        )
        management_cred = AzureIdentityCredentialAdapter()
        management_cred.set_token()
        graph_rbac_creds = AzureIdentityCredentialAdapter(resource_id="https://graph.windows.net/")
        graph_rbac_creds.set_token()
    except ClientAuthenticationError:
        # NOTE: Default Azure Credential raises its own error
        raise ExitException("Please try again after logging into azure in your terminal")

    # Delete Machine Types and Model Servers on cluster first
    cluster_utils.echo_delimiter()
    with api_client_exception_handler():
        click.echo(
            "Sending message to Spell to remove all Machine Types "
            "from the cluster {}...".format(cluster["name"])
        )
        spell_client.delete_cluster_contents(cluster["name"])

    # Block until cluster is drained. This is necessary because the API will fail to
    # drain if we delete the IAM role before the machine types are marked as drained
    cluster_utils.block_until_cluster_drained(spell_client, cluster["name"])

    subscription_id = cluster["role_credentials"]["azure"]["subscription_id"]
    tenant_id = cluster["role_credentials"]["azure"]["tenant_id"]
    resource_client = ResourceManagementClient(credentials, subscription_id)
    rg_name = cluster["networking"]["azure"]["resource_group_name"]

    # Delete Resource group and everything in it
    cluster_utils.echo_delimiter()
    if not click.confirm(
        "WARNING: All the stored run outputs and uploads will be deleted with this command, as they are within "
        "the cluster's resource group. If you would like to save this data, please copy it to a different storage "
        "account in a different resource group before re-running this command. Continue?"
    ):
        return
    click.echo("Deleting Resource Group...")
    delete_async_operation = resource_client.resource_groups.begin_delete(rg_name)
    delete_async_operation.wait()

    # Delete App/SP
    cluster_utils.echo_delimiter()
    click.echo("Deleting App and Service Principal")
    client = GraphRbacManagementClient(graph_rbac_creds, tenant_id)
    client.service_principals.delete(cluster["role_credentials"]["azure"]["sp_object_id"])
    client.applications.delete(cluster["role_credentials"]["azure"]["app_object_id"])
    click.echo("Deleted App and Service Principal `spell-app`")

    # Last step is to mark the cluster as deleted
    cluster_utils.echo_delimiter()
    with api_client_exception_handler():
        spell_client.delete_cluster(cluster["name"])
        click.echo("Successfully deleted cluster on Spell")
