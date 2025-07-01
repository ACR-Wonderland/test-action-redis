import json
import argparse
from upstash_redis import Redis

def token_exists(redis, token: str) -> bool:
    key = f"token:{token}"
    result = redis.get(key)
    return result is not None

def create_token(redis, token: str, quota: int = 10):
    key = f"token:{token}"
    value = {"token": token, "quota": quota}
    redis.set(key, json.dumps(value))
    print(f"✅ Token '{token}' created with quota {quota}")

def get_token_quota(redis, token: str) -> int:
    key = f"token:{token}"
    result = redis.get(key)
    if result is None:
        raise Exception("Token not found.")
    return json.loads(result)["quota"]

def decrement_token_quota(redis, token: str):
    key = f"token:{token}"
    result = redis.get(key)
    if result is None:
        return False, 0

    data = json.loads(result)
    quota = data.get("quota", 0)

    if quota <= 0:
        return False, 0

    data["quota"] = quota - 1
    redis.set(key, json.dumps(data))
    return True, data["quota"]

parser = argparse.ArgumentParser(description="Process token and Redis credentials.")
parser.add_argument("--token", type=str, required=True, help="GitHub token")
parser.add_argument("--redis-url", type=str, required=True, help="Upstash Redis REST URL")
parser.add_argument("--redis-token", type=str, required=True, help="Upstash Redis REST Token")
args = parser.parse_args()

redis = Redis(
    url=args.redis_url,
    token=args.redis_token
)

token = args.token

if not token_exists(redis, token):
    create_token(redis, token)

allowed, remaining = decrement_token_quota(redis, token)
if allowed:
    print(f"✅ Allowed. Remaining quota: {remaining}")
else:
    print("🚫 Too many requests. Quota exhausted.")
