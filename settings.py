from os import getenv

# 기본 설정값을 생성한다.
# 그리고 환경변수에 있으면 불러온다.
# 출력값은 dictionary 이다.
def generateDefaultSetting():
    p_settings = {
        "REDIS" : getenv("REDIS"),
        "REDIS_PORT" : getenv("REDIS_port"),
        "REDIS_PASSWORD" : getenv("REDIS_PASSWORD"),
        "RW_WORKERS" : getenv("RW_WORKERS"),
        "MODE" : getenv("CRAWLER_MODE")
    }

    res = {}
    for k,v in p_settings.items():
        # 환경변수에서 있나 없나
        if v == None:
            # 없으면 기본값 집어넣기
            if k == "REDIS":
                res[k] = "127.0.0.1"
            elif k == "REDIS_PORT":
                res[k] = 6379
            elif k == "RW_WORKERS":
                res[k] = 20
            elif k == "MODE":
                res[k] = "api"
            else:
                res[k] = None
        else:
            # 환경변수에서 int로 처리해야 하는 것 있으면 처리한다.
            if k == "REDIS_PORT" or k == "RW_WORKERS":
                res[k] = int(v)
            else:
                res[k] = v

    return res

