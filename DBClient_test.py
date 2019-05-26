from settings import generateDefaultSetting
from DBClient import DBClient
from BoardCode import HAKSA

def dbLogin():
    setting = generateDefaultSetting()
    return DBClient(setting, HAKSA)

if __name__ == "__main__":
    db = dbLogin()
    keys = db.keys(True)
    # sync_test.py 를 작동 후 실행을 가정
    print(keys[0], keys[-1])
    print(db.get(1))
    print(db.get(keys[-1], False))
    print(keys[len(keys)-3:len(keys)])
    for i in range(len(keys)):
        assert i+1 == keys[i]

