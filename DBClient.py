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

    # key 값은 그대로 놓고 value만 json으로 변환해서 저장한다.
    def set(self, key, value):
        Redis.set(self, key, json.dumps(value, ensure_ascii=False))

    # key 값은 그대로 놓고 결과값만 json에서 python 구조체로 변환해서 볼러온다.
    # python 자료형인지 string으로 변환할지 결정한다.(기본값 python 자료형)
    def get(self, key, trans=True):
        res = Redis.get(self, key).decode("utf-8")
        return json.loads(res) if trans else res

    # 키의 타입은 숫자로 이뤄져 있어 간편함을 위해 int로 변환해주고
    # 필요시 정렬한다.
    def keys(self, sort=False):
        res = list(map(int, Redis.keys(self)))
        if sort:
            res.sort()
        return res
