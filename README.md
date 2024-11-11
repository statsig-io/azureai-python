# Statsig Azure AI
[![tests](https://github.com/statsig-io/azureai-python/actions/workflows/test.yml/badge.svg)](https://github.com/statsig-io/azureai-python/actions/workflows/test.yml)

Azure AI library with a built-in Statsig SDK.

Statsig helps you move faster with Feature Gates (Feature Flags) and Dynamic Configs. It also allows you to run A/B tests to validate your new features and understand their impact on your KPIs. If you're new to Statsig, create an account at [statsig.com](https://www.statsig.com).

## Getting Started
1. Install the library `pip install azureai-statsig`
2. Initialize the main AzureAI interface along with the internal Statsig service
```python
AzureAI.initialize(<STATSIG_SERVER_KEY>, StatsigOptions(tier="development"))
```
3. Create the AzureAI inference client
```python
client = AzureAI.get_model_client_from_endpoint(<DEPLOYMENT_ENDPOINT_URL>, <DEPLOYMENT_KEY>)
```
Optionally, use a Statsig Dynamic Config to provide default configurations
```python
client = AzureAI.get_model_client("azureai_model", <DEPLOYMENT_ENDPOINT_URL>, <DEPLOYMENT_KEY>)
```
4. Call the API
```python
response = client.complete([
    SystemMessage(content="You are a helpful assistant."),
    UserMessage(content="Give me 5 good reasons why I should exercise every day.")
])
```

## References
- Azure AI SDK [documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-inference-readme?view=azure-python-preview)
- Statsig SDK [documentation](https://docs.statsig.com/server/pythonSDK/)