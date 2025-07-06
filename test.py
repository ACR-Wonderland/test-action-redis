import json
import argparse
import os
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

parser = argparse.ArgumentParser(description="Process token.")
parser.add_argument("--token", type=str, required=True, help="GitHub token")
args = parser.parse_args()

# Get Redis credentials from environment variables
redis_url = os.environ.get("UPSTASH_REDIS_REST_TOKEN")
redis_token = os.environ.get("UPSTASH_REDIS_REST_URL")

if not redis_url or not redis_token:
    raise Exception("REDIS_URL and REDIS_TOKEN environment variables must be set.")

redis = Redis(
    url=redis_url,
    token=redis_token
)

token = os.getenv("GITHUB_ACTOR", args.token)

if not token_exists(redis, token):
    create_token(redis, token)

allowed, remaining = decrement_token_quota(redis, token)
if allowed:
    print(f"✅ Allowed. Remaining quota: {remaining}")
else:
    print("🚫 Too many requests. Quota exhausted.")
