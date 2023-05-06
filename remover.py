import fnmatch
import os
from datetime import datetime
from pathlib import Path


def lookupRemovable():
    dir_path = str(Path(__file__).parent / "backups")

    filename_pattern = "backup-*-*.e"
    yfilename_pattern = "ybackup-*-*.e"
    wfilename_pattern = "wbackup-*-*.e"
    mfilename_pattern = "mbackup-*-*.e"

    now = datetime.now()

    removableBackups = set()
    for filename in os.listdir(dir_path):
        file_date = datetime.strptime(filename.split("-")[1], "%d.%m.%Y")
        if fnmatch.fnmatch(filename, filename_pattern):
            if (now - file_date).days > 7:
                removableBackups.add(filename)
        elif fnmatch.fnmatch(filename, yfilename_pattern):
            if (now - file_date).days > 366:
                removableBackups.add(filename)
        elif fnmatch.fnmatch(filename, mfilename_pattern):
            if (now - file_date).days > 360:
                removableBackups.add(filename)
        elif fnmatch.fnmatch(filename, wfilename_pattern):
            if (now - file_date).days > 30:
                removableBackups.add(filename)

    for bk in removableBackups:
        remove(bk)


def getBackupsList():
    backupsPath = str(Path(__file__).parent / "backups")
    currentBackupsList = os.listdir(backupsPath)
    return set(currentBackupsList)


def remove(bk):
    path = str(Path(__file__).parent / "backups/")
    os.remove(path + "/" + bk)
    sender = str(Path(__file__).parent / "sender.py")
    os.system(
        'python3 {} "Se ha <b>eliminado</b> una copia de seguridad antigua: {}"'.format(
            sender, bk
        )
    )


def getBackupDate(bk):
    day, month, year = bk[1:].lstrip("backup-").split("-")[0].split(".")
    date = datetime(day=int(day), month=int(month), year=int(year))
    return date.timetuple().tm_yday, date.month, date.year


if __name__ == "__main__":
    lookupRemovable()
