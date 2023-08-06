import asyncio
from functools import wraps
import importlib
from pathlib import Path
import sys
from typing import Awaitable, Callable, Union

from httpx import RequestError, Response as HttpxResponse

from spell.serving.exceptions import InvalidPredictor

# This makes the max wait 960ms
RETRY_ATTEMPTS = 5
RETRY_BASE_WAIT_MS = 60


def import_user_module(
    module_path: Union[Path, str],
    python_path: Union[Path, str],
):
    # module_path is the path in the filesystem to the module
    # python_path is the python path to the predictor in the form path.to.module
    validate_python_path(python_path)
    sys.path.append(str(module_path))  # Path objects can't be used here
    importlib.import_module(python_path)


def validate_python_path(python_path: str):
    split_python_path = python_path.split(".")
    if split_python_path[0] == "spell":
        raise InvalidPredictor('Top-level module for predictor cannot be named "spell"')
    invalid_path_identifier = next(
        (identifier for identifier in split_python_path if not identifier.isidentifier()), None
    )
    if invalid_path_identifier:
        raise InvalidPredictor(f"Invalid python path element {invalid_path_identifier}")


def retry(url: str) -> Callable:
    """An async exponential backoff decorator"""

    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs) -> Awaitable[HttpxResponse]:
            num_attempts = 0
            error = None
            while num_attempts <= RETRY_ATTEMPTS:
                try:
                    return await f(*args, **kwargs)
                except RequestError as e:
                    num_attempts += 1
                    error = e
                    msg = f"ERROR: Got error {e} on {url} on attempt {num_attempts}."
                    if num_attempts < RETRY_ATTEMPTS:
                        wait_time = RETRY_BASE_WAIT_MS * 2 ** num_attempts
                        print(f"{msg} Retrying in {wait_time}ms...")
                        await asyncio.sleep(wait_time / 1000)
                    else:
                        print(msg)
                        break
            raise error

        return wrapper

    return decorator
