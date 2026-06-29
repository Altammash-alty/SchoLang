import os
import json
from upstash_redis import Redis

# Upstash Redis client — free tier at upstash.com
# Add these two keys to your .env after creating an Upstash account
redis = Redis(
    url   = os.getenv("UPSTASH_REDIS_REST_URL"),
    token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
)

SUMMARY_EXPIRE = 60 * 60 * 24 * 30   # 30 days in seconds
IDEAS_EXPIRE   = 60 * 60 * 24 * 30   # 30 days in seconds


def summary_key(doi: str, language: str) -> str:
    # Unique cache key per paper per language
    # e.g. "summary:10.1234/example:hi"
    clean_doi = doi.replace("/", "_").replace(":", "_")
    return f"summary:{clean_doi}:{language}"


def ideas_key(doi: str, language: str) -> str:
    clean_doi = doi.replace("/", "_").replace(":", "_")
    return f"ideas:{clean_doi}:{language}"


async def get_cached_summary(doi: str, language: str) -> dict | None:
    try:
        key  = summary_key(doi, language)
        data = redis.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print(f"Redis get summary error: {e}")
    return None


async def set_cached_summary(doi: str, language: str, summary: dict) -> None:
    try:
        key = summary_key(doi, language)
        redis.setex(key, SUMMARY_EXPIRE, json.dumps(summary))
    except Exception as e:
        print(f"Redis set summary error: {e}")


async def get_cached_ideas(doi: str, language: str) -> list | None:
    try:
        key  = ideas_key(doi, language)
        data = redis.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print(f"Redis get ideas error: {e}")
    return None


async def set_cached_ideas(doi: str, language: str, ideas: list) -> None:
    try:
        key = ideas_key(doi, language)
        redis.setex(key, IDEAS_EXPIRE, json.dumps(ideas))
    except Exception as e:
        print(f"Redis set ideas error: {e}")