import os
import unittest

from statsig.statsig_options import StatsigOptions
from azureai.azure_ai import AzureAI

STATSIG_SERVER_KEY = os.environ["STATSIG_SERVER_KEY"]
DEPLOYMENT_ENDPOINT_URL = os.environ["EMBEDDINGS_DEPLOYMENT_ENDPOINT_URL"]
DEPLOYMENT_KEY = os.environ["EMBEDDINGS_DEPLOYMENT_KEY"]


class TestEmbeddings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        AzureAI.initialize(STATSIG_SERVER_KEY, StatsigOptions(tier="development"))
        cls.client = AzureAI.get_model_client_from_endpoint(DEPLOYMENT_ENDPOINT_URL, DEPLOYMENT_KEY)

    @classmethod
    def tearDownClass(cls) -> None:
        AzureAI.shutdown()

    def test_embeddings(self):
        response = self.client.get_embeddings(["Hello, world!", "Goodbye, world!"])
        self.assertIsNotNone(response, "Expected response to not be None")
        self.assertGreater(len(response.data), 0, "Expected at least 1 embedding")
        print()  # newline
        for item in response.data:
            length = len(item.embedding)
            print(
                f"data[{item.index}]: length={length}, [{item.embedding[0]}, {item.embedding[1]}, "
                f"..., {item.embedding[length-2]}, {item.embedding[length-1]}]"
            )
