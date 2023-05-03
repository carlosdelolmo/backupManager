import os
from pathlib import Path


def deleteFolder():
    path = str(Path(__file__).parent)
    os.system(path)

def deleteFromCrontab():
    user = os.environ.get("USER")
    os.system("crontab -l | grep -v '/usr/bin/python3 /home/{}/backupManager/telegram_bot.py.*@reboot$' | crontab -".format(user))
    os.system("crontab -l | grep -v '/usr/bin/python3 /home/{}/backupManager/backup.py b.*59 23 \* \* \*$' | crontab -".format(user))
if __name__ == "__main__":
    deleteFromCrontab()
    deleteFolder()