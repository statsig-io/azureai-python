from typing import Optional
from statsig import statsig, StatsigOptions
from .get_statsig_user import get_statsig_user
from .model_client import ModelClient


class AzureAI:
    @staticmethod
    def initialize(secret_key: str, options: Optional[StatsigOptions] = None):
        statsig.initialize(secret_key=secret_key, options=options)

    @staticmethod
    def get_model_client_from_endpoint(api_endpoint: str, api_key: str):
        return ModelClient(
            endpoint=api_endpoint,
            api_key=api_key,
        )

    @staticmethod
    def get_model_client(
        config_name: str,
        default_endpoint: Optional[str],
        default_key: Optional[str]
    ):
        config = statsig.get_config(get_statsig_user(), config_name)
        endpoint = config.get_typed("endpoint", default_endpoint)
        api_key = config.get_typed("key", default_key)
        completion_defaults = config.get_typed("completion_defaults", {})

        return ModelClient(
            endpoint=endpoint,
            api_key=api_key,
            completion_defaults=completion_defaults
        )

    @staticmethod
    def get_statsig_server() -> statsig:
        return statsig

    @staticmethod
    def shutdown():
        statsig.shutdown()
