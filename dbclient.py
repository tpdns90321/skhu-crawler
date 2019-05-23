import sys
from redis import Redis
import json

# 설정값과 보드코드로 Redis에 접근하는 클래스이다.
class DBClient(Redis):
    def __init__(self, Settings, BoardCode):
        Redis.__init__(self,
                       host=Settings["redis"],
                       port=Settings["redis-port"],
                       password=Settings["redis-password"],
                       db=BoardCode["dbid"])
    def set(self, key, value):
        Redis.set(self, key, json.dumps(value, ensure_ascii=False))

    def get(self, key):
        return json.loads(Redis.get(self, key).decode("utf-8"))
