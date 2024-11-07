from typing import Optional
from statsig import StatsigUser


def get_statsig_user(user: Optional[StatsigUser] = None) -> StatsigUser:
    if user is not None:
        user.custom_ids["sdk_type"] = "azureai-python"
        return user

    return StatsigUser(custom_ids={"sdk_type": "azureai-python"})
