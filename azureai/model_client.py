import time

from typing import Dict, Iterable, List, Optional, Union, Callable
from azure.ai.inference import ChatCompletionsClient, EmbeddingsClient
from azure.ai.inference.models._models import (
    ChatRequestMessage,
    ChatCompletions,
    StreamingChatCompletionsUpdate,
    ModelInfo,
    EmbeddingsResult,
    EmbeddingInput
)
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from statsig import statsig, StatsigUser, StatsigEvent
from .get_statsig_user import get_statsig_user


class InvokeContext:
    invoke_time: float

    def __init__(self):
        self.invoke_time = time.time()


class ModelClient:
    def __init__(self, endpoint: str, api_key: str, completion_defaults: Optional[dict] = {}):
        self.completion_defaults = completion_defaults
        self.completions_client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key),
            **completion_defaults
        )
        self.embeddings_client = EmbeddingsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key),
            **completion_defaults
        )

    def complete(
        self,
        messages: List[ChatRequestMessage],
        options: Optional[dict] = {},
        user: Optional[StatsigUser] = None
    ) -> Optional[ChatCompletions]:
        def task():
            invoke_context = self.log_invoke(user, "complete")
            res = self.completions_client.complete(stream=False, messages=messages, **options)

            self.handle_errors(res)
            self.log_usage(
                user,
                "complete",
                {
                    "model": res.model,
                    "completion_tokens": res.usage.completion_tokens,
                    "prompt_tokens": res.usage.prompt_tokens,
                    "total_tokens": res.usage.total_tokens,
                    "created": res.created
                },
                invoke_context
            )
            return res
        return self.handle_errors(task=task, fallback=None)

    def stream_complete(
        self,
        messages: List[ChatRequestMessage],
        options: Optional[dict] = {},
        user: Optional[StatsigUser] = None
    ) -> Optional[Iterable[StreamingChatCompletionsUpdate]]:
        def task():
            invoke_context = self.log_invoke(user, "stream")
            res = self.completions_client.complete(stream=True, messages=messages, **options)

            self.log_usage(user, "stream_begin", {}, invoke_context)
            stream_start_ms = round(time.time() * 1000)
            model = None
            for update in res:
                model = update.model
            self.log_usage(
                user,
                "stream_end",
                {
                    "stream_time_ms": round(time.time() * 1000) - stream_start_ms,
                    "model": model
                },
                invoke_context
            )
            return res
        return self.handle_errors(task=task, fallback=None)

    def get_info(self, user: Optional[StatsigUser] = None) -> Optional[ModelInfo]:
        def task():
            invoke_context = self.log_invoke(user, "getInfo")
            res = self.completions_client.get_model_info()

            self.log_usage(
                user,
                "getInfo",
                {
                    "model_name": res.model_name,
                    "model_provider_name": res.model_provider_name,
                    "model_type": res.model_type
                },
                invoke_context
            )
            return res
        return self.handle_errors(task=task, fallback=None)

    def get_embeddings(
        self,
        input: List[EmbeddingInput],
        options: Optional[dict] = {},
        user: Optional[StatsigUser] = None,
    ) -> Optional[EmbeddingsResult]:
        def task():
            invoke_context = self.log_invoke(user, "getEmbeddings")
            res = self.embeddings_client.embed(input=input, **options)

            self.handle_errors(res)
            self.log_usage(
                user,
                "getEmbeddings",
                {
                    "model": res.model,
                    "prompt_tokens": res.usage.prompt_tokens,
                    "total_tokens": res.usage.total_tokens,
                    "embedding_length": len(res.data)
                },
                invoke_context
            )
            return res
        return self.handle_errors(task=task, fallback=None)

    def handle_errors[T](self, task: Callable[[], T], fallback: T) -> T:
        try:
            return task()
        except HttpResponseError as e:
            print(f"Status code: {e.status_code} ({e.reason})")
            print(e.message)
            return fallback

    def scrub_defaults(self):
        if self.completion_defaults["max_tokens"] == 0:
            del self.completion_defaults["max_tokens"]
        if self.completion_defaults["stop"] is None or self.completion_defaults["stop"] is False:
            del self.completion_defaults["stop"]

    def log_invoke(self, user: Optional[StatsigUser], method: str) -> InvokeContext:
        event = StatsigEvent(
            user=get_statsig_user(user),
            event_name="invoke",
            value=method
        )
        statsig.log_event(event)
        return InvokeContext()

    def log_usage(
        self,
        user: Optional[StatsigUser],
        method: str,
        usage: Dict[str, Union[str, int]],
        context: Optional[InvokeContext]
    ):
        event = StatsigEvent(
            user=get_statsig_user(user),
            event_name="usage",
            value=method,
            metadata=usage
        )

        if context is not None:
            event.metadata["latency_ms"] = time.time() - context.invoke_time

        statsig.log_event(event)
