import redis, os, json

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB   = int(os.getenv("REDIS_DB", 0))

redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

def set_cache(key: str, value, ttl: int = 3600):
    redis_client.setex(key, ttl, json.dumps(value))
    print("Setting inside reddis")


def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        print("Its returning data")
        return json.loads(data)
    else:
        print("Its returning None")
        None
    