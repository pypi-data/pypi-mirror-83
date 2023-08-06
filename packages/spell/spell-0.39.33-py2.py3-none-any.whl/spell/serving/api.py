from collections import namedtuple
import importlib
from pathlib import Path
import sys
from typing import Dict, Optional, Union

from starlette.requests import Request
from starlette.responses import Response

from spell.serving import BasePredictor
from spell.serving.exceptions import InvalidPredictor
from spell.serving.types import APIResponse, PredictorClass

ModelInfo = namedtuple("ModelInfo", ("name", "version"), defaults=(None, None))


class API:
    FILE_IMPORT_NAME = "spell_predictor"

    def __init__(self, predictor_class: PredictorClass) -> None:
        self.predictor_class = predictor_class
        self.predict_arg_generator = self.predictor_class.get_predict_argument_generator()
        self.health_arg_generator = self.predictor_class.get_health_argument_generator()
        self.predictor = None

    @classmethod
    def from_module(
        cls,
        module_path: Union[Path, str],
        python_path: Union[Path, str],
        classname: Optional[str] = None,
    ):
        # module_path is the path in the filesystem to the module
        # python_path is the python path to the predictor in the form path.to.module
        cls.validate_python_path(python_path)
        sys.path.append(str(module_path))  # Path objects can't be used here
        importlib.import_module(python_path)
        predictor_class = cls.get_predictor_class(classname)
        return cls(predictor_class)

    @classmethod
    def get_predictor_class(cls, classname: Optional[str]) -> PredictorClass:
        predictors = {p.__name__: p for p in BasePredictor.__subclasses__()}
        if not predictors:
            raise InvalidPredictor(
                "No predictors found. Make sure your predictors extend BasePredictor."
            )
        if not classname:
            if len(predictors) > 1:
                raise InvalidPredictor(
                    "More than one predictor found, but no classname was specified."
                )
            predictor_name = next(iter(predictors))
            return predictors[predictor_name]
        try:
            return predictors[classname]
        except KeyError:
            raise InvalidPredictor(
                f"No predictor named {classname} was found. The predictors found were ({', '.join(predictors)})"
            )

    @staticmethod
    def validate_python_path(python_path: str):
        split_python_path = python_path.split(".")
        if split_python_path[0] == "spell":
            raise InvalidPredictor('Top-level module for predictor cannot be named "spell"')
        invalid_path_identifier = next(
            (identifier for identifier in split_python_path if not identifier.isidentifier()), None
        )
        if invalid_path_identifier:
            raise InvalidPredictor(f"Invalid python path element {invalid_path_identifier}")

    def initialize_predictor(self, config: Dict) -> None:
        model_info = config.get("model_info", {})
        user_config = config.get("user_config", {})
        self.predictor = self.predictor_class(**user_config)
        if not hasattr(self.predictor, "model_info"):
            self.predictor.model_info = ModelInfo(**model_info)

    async def predict(self, request: Request) -> APIResponse:
        kwargs, tasks = await self.predict_arg_generator(request)
        if isinstance(kwargs, Response):  # Indicating an error response
            return kwargs, tasks
        return self.predictor.predict(**kwargs), tasks

    async def health(self, request: Request) -> APIResponse:
        kwargs, tasks = await self.health_arg_generator(request)
        return self.predictor.health(**kwargs), tasks
