import gevent
import sys

from sync import Sync
from settings import generateDefaultSetting
from BoardCode import HAKSA

if __name__ == "__main__":
    setting = generateDefaultSetting()
    sync = Sync(setting, HAKSA)
    if len(sys.argv) > 1 and sys.argv[1] == "firstRun":
        sync.firstRun()
        print(len(sync.keys()))

    keys = len(sync.keys())
    [sync.delete(i) for i in range(keys-3,keys+1)]
    print(len(sync.keys()))
    sync.Run()
    print(len(sync.keys()))

