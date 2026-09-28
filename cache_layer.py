import redis
import json
import hashlib

r = redis.Redis(host="redis", port=6379, decode_responses=True )

def cache_key(strs):
	return hashlib.md5(json.dumps(sorted(strs)).encode()).hexdigest()

def get_cached(strs):
	key = cache_key(strs)
	cached = r.get(key)

	if cached:
		return json.loads(cached)
	else:
		return None

def set_cache(strs, result, ttl=300):
	key = cache_key(strs)
	r.setex(key, ttl, json.dumps(result))