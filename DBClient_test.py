from settings import generateDefaultSetting
from DBClient import DBClient
from BoardCode import HAKSA

def dbLogin():
    setting = generateDefaultSetting()
    return DBClient(setting, HAKSA)

if __name__ == "__main__":
    db = dbLogin()
    keys = db.keys(True)
    print(keys[0], keys[-1])
    print(db.get(1))
    print(db.get(keys[-1], False))
    print(keys[len(keys)-3:len(keys)])

