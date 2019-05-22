import redis

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
print(str(r.get("1")))
