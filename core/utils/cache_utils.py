from django.core.cache import caches
from functools import wraps
import json

def cache_result(prefix, timeout=300):
    \"\"\"Decorator to cache function results with a given prefix and timeout.\"\"\"
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = caches['default']
            cache_key = f\"{prefix}:{json.dumps(kwargs, sort_keys=True)}\"
            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator

def invalidate_cache(prefix, **kwargs):
    \"\"\"Invalidate cache for a specific prefix and key-value pairs.\"\"\"
    cache = caches['default']
    if kwargs:
        cache_key = f\"{prefix}:{json.dumps(kwargs, sort_keys=True)}\"
        cache.delete(cache_key)
    else:
        # If no kwargs, delete all keys with this prefix
        cache.delete_many(keys=[f\"{prefix}:{key}\" for key in cache.keys(f\"{prefix}:*\")])
