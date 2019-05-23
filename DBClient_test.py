from settings import generateDefaultSetting
from DBClient import DBClient
from BoardCode import HAKSA

def dbLogin():
    setting = generateDefaultSetting()
    return DBClient(setting, HAKSA)

if __name__ == "__main__":
    db = dbLogin()
    keys = db.keys()
    keys = list(map(int, keys))
    keys.sort()
    print(keys[0], keys[-1])
    print(db.get(1))
    print(db.get(901, False))

