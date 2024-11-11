import os
import unittest

from statsig.statsig_options import StatsigOptions
from azure.ai.inference.models import SystemMessage, UserMessage
from azureai.model_client import ModelClient
from azureai.azure_ai import AzureAI

ENVIRONMENT_TIER = os.environ["ENVIRONMENT_TIER"]
STATSIG_SERVER_KEY = os.environ["STATSIG_SERVER_KEY"]
DEPLOYMENT_ENDPOINT_URL = os.environ["COMPLETIONS_DEPLOYMENT_ENDPOINT_URL"]
DEPLOYMENT_KEY = os.environ["COMPLETIONS_DEPLOYMENT_KEY"]


class TestCompletions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        AzureAI.initialize(STATSIG_SERVER_KEY, StatsigOptions(tier=ENVIRONMENT_TIER))
        cls.client = ModelClient(DEPLOYMENT_ENDPOINT_URL, DEPLOYMENT_KEY)

    @classmethod
    def tearDownClass(cls) -> None:
        AzureAI.shutdown()

    def test_completions(self):
        response = self.client.complete([
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content="Give me 5 good reasons why I should exercise every day.")
        ])
        self.assertIsNotNone(response, "Expected response to not be None")
        print()  # newline
        for item in response.choices:
            content = item.message.content
            self.assertGreater(len(content), 0, "Expected non-empty content")
            print(content)

    def test_completions_stream(self):
        response = self.client.stream_complete([
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content="Give me 5 good reasons why I should exercise every day.")
        ])
        self.assertIsNotNone(response, "Expected response to not be None")
        responses = 0
        print()  # newline
        for update in response:
            responses += 1
            print(update.choices[0].delta.content or "", end="", flush=True)

        self.assertGreater(responses, 0, "Expected at least one response")
