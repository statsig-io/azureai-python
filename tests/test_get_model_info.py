import os
import unittest

from statsig.statsig_options import StatsigOptions
from azureai.model_client import ModelClient
from azureai.azure_ai import AzureAI

ENVIRONMENT_TIER = os.environ["ENVIRONMENT_TIER"]
STATSIG_SERVER_KEY = os.environ["STATSIG_SERVER_KEY"]
DEPLOYMENT_ENDPOINT_URL = os.environ["MODEL_INFO_DEPLOYMENT_ENDPOINT_URL"]
DEPLOYMENT_KEY = os.environ["MODEL_INFO_DEPLOYMENT_KEY"]


class TestGetModelInfo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        AzureAI.initialize(STATSIG_SERVER_KEY, StatsigOptions(tier=ENVIRONMENT_TIER))
        cls.client = ModelClient(DEPLOYMENT_ENDPOINT_URL, DEPLOYMENT_KEY)

    @classmethod
    def tearDownClass(cls) -> None:
        AzureAI.shutdown()

    def test_get_model_info(self):
        model_info = self.client.get_info()
        self.assertIsNotNone(model_info, "Expected model info to not be None")
        print()  # newline
        print(f"Model name: {model_info.model_name}")
        print(f"Model provider name: {model_info.model_provider_name}")
        print(f"Model type: {model_info.model_type}")
