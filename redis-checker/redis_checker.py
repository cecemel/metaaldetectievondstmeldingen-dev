"""
Helpscript to verify if redis is ready
"""
import time
import redis


def _is_redis_ready():
    redis_client = redis.Redis(host='redis')
    try:
        redis_client.get(None)  # getting None returns None or throws an exception
    except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError):
        return False
    return True


if __name__ == '__main__':
    max_attempts = 20
    attempts = 0
    while not _is_redis_ready() or attempts > max_attempts:
        print("redis not ready, waiting..")
        attempts += 1
        time.sleep(10)

    if attempts > max_attempts:
        print("redis not ready, giving up")
        exit(1)
