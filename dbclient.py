import redis

# 설정값과 보드코드로 Redis에 접근하는 클래스이다.
class DBClient(redis.Redis):
    def __init__(self, Settings, BoardCode):
        redis.Redis.__init__(self,
                             host=Settings["redis"],
                             port=Settings["redis-port"],
                             password=Settings["redis-password"],
                             db=BoardCode["dbid"])
