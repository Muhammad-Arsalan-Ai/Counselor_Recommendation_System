import redis  # type: ignore


def get_redis_client() -> redis.client.Redis:
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    return redis_client
