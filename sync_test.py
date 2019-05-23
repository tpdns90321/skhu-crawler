from sync import Sync
from settings import generateDefaultSetting
from BoardCode import HAKSA

if __name__ == "__main__":
   setting = generateDefaultSetting()
   setting["rw-workers"] = 30
   sync = Sync(setting, HAKSA)
   sync.firstRun()
