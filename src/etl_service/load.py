import json

import redis  # type: ignore

from base_logger import logger
from redis_connector import get_redis_client
from transform import data_transformations


def load_data_to_redis(
    redis_client: redis.client.Redis, specializations_dfs: dict
) -> dict:
    """
    Stores specializations_dfs that is given by data_transformations function in Redis,
    using redis_client that is given by get_redis_client function.

    Parameters:
    - redis_client: redis.client.Redis
        redis_client object given by get_redis_client function.
    - specializations_dfs: dict
        A dictionary containing specializations (key) dataframes (value).

    Preconditions:
    - The `data_transformations()` function should be called before load_data_to_redis to get data from transform.py
    - The `get_redis_client()` function should be called before load_data_to_redis to get redis_client from
      redis_connector.py

    Returns:
    dict: The same input dictionary of specializations dataframes.
    """

    for key, val in specializations_dfs.items():
        redis_client.set(key, json.dumps(val, indent=2))
    logger.info("Data Stored in Redis.")
    return specializations_dfs

if __name__ == "__main__":
    load_data_to_redis(get_redis_client(), data_transformations())
