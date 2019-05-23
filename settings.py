from os import getenv

def generateDefaultSetting():
    p_settings = {
        "redis" : getenv("redis"),
        "redis-port" : getenv("redis-port"),
        "redis-password" : getenv("redis-password"),
        "rw-workers" : getenv("rw-workers"),
        "mode" : getenv("crawler-mode")
    }

    res = {}
    for k,v in p_settings.items():
        if v == None:
            if k == "redis":
                res[k] = "127.0.0.1"
            elif k == "redis-port":
                res[k] = 6379
            elif k == "rw-workers":
                res[k] = 20
            elif k == "mode":
                res[k] = "api"
            else:
                res[k] = None
        else:
            if k == "redis-port" or k == "rw-workers":
                res[k] = int(v)
            else:
                res[k] = v

    return res

