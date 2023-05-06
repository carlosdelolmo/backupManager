import os
import datetime
import sys
from pathlib import Path
import toml


def dobackup():
    backupsDir = str(Path(__file__).parent / "backups")
    if not os.path.exists(backupsDir):
        os.mkdir(backupsDir)
    backupMap = getCompleteBackupsMap()
    (
        lastYBackupDate,
        lastMBackupDate,
        lastWBackupDate,
    ) = getLastCompleteFilteredBackupList(backupMap)
    diffY = calculateDiffDate(lastYBackupDate[-1]) if len(lastYBackupDate) > 0 else 361
    diffM = calculateDiffDate(lastMBackupDate[-1]) if len(lastMBackupDate) > 0 else 361
    diffW = calculateDiffDate(lastWBackupDate[-1]) if len(lastWBackupDate) > 0 else 361
    if diffY > 360:
        completeBackup("y")
    elif diffM > 30:
        completeBackup("m")
    elif diffW > 7:
        completeBackup("w")
    else:
        incrBackup()


def calculateDiffDate(file):
    dt = datetime.datetime.now()
    return (dt - datetime.datetime.strptime(file, "%d/%m/%Y")).days


def completeBackup(type):
    dt = datetime.datetime.now()
    backupFileName = "{}backup-{:02}.{:02}.{:02}-{:02}.{:02}.{:02}".format(
        type, dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second
    )
    backupsDir = str(Path(__file__).parent / "backups")
    newpath = str(backupsDir + "/" + backupFileName)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "backup_files")
    original_files_f = open(filename, "r")
    original_files_l = original_files_f.readlines()
    bkpfiles = ""
    for f in original_files_l:
        f = f.strip(" ").strip("\n").strip("\t").strip(" ")
        if (
            (not f in [".", "..", "", "\n", "\t", " "])
            and not f.startswith("//")
            and f.startswith("/")
        ):
            bkpfiles += f + " "

    snarFile = str(Path(__file__).parent / "backup.snar")
    if os.path.exists(snarFile) and not os.path.isdir(snarFile):
        os.system("rm {}".format(snarFile))

    os.system(
        "tar -czf {}.tar --listed-incremental={} {} >/dev/null 2>/dev/null".format(
            newpath, snarFile, bkpfiles
        )
    )
    cypher = str(Path(__file__).parent / "cypher.py")
    remover = str(Path(__file__).parent / "remover.py")
    sender = str(Path(__file__).parent / "sender.py")
    os.system(
        'python3 {} e {} && python3 {} "Se ha creado una copia de seguridad nueva: <code>{}</code>"'.format(
            cypher, newpath + ".tar", sender, backupFileName
        )
    )
    os.system("python3 {}".format(remover))
    checkDisk()


def incrBackup():
    dt = datetime.datetime.now()
    backupFileName = "backup-{:02}.{:02}.{:02}-{:02}.{:02}.{:02}".format(
        dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second
    )
    backupsDir = str(Path(__file__).parent / "backups")
    snarFile = str(Path(__file__).parent / "backup.snar")
    newpath = str(backupsDir + "/" + backupFileName)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "backup_files")
    original_files_f = open(filename, "r")
    original_files_l = original_files_f.readlines()
    bkpfiles = ""
    for f in original_files_l:
        f = f.strip(" ").strip("\n").strip("\t").strip(" ")
        if (
            (not f in [".", "..", "", "\n", "\t", " "])
            and not f.startswith("//")
            and f.startswith("/")
        ):
            bkpfiles += f + " "
    os.system(
        "tar -czf {}.tar --listed-incremental={} --level=1 {} >/dev/null 2>/dev/null".format(
            newpath, snarFile, bkpfiles
        )
    )
    cypher = str(Path(__file__).parent / "cypher.py")
    sender = str(Path(__file__).parent / "sender.py")
    remover = str(Path(__file__).parent / "remover.py")
    os.system(
        'python3 {} e {} && python3 {} "Se ha creado una copia de seguridad nueva: <code>{}</code>"'.format(
            cypher, newpath + ".tar", sender, backupFileName
        )
    )
    os.system("python3 {}".format(remover))
    checkDisk()


def checkDisk():
    size, maxSizeGb = getBackupsSizeGb()
    if size > 0.7 * maxSizeGb:
        sender = str(Path(__file__).parent / "sender.py")
        os.system(
            'python3 {} "El tamaño de las copias de seguridad es elevado: {} GB, {}%"'.format(
                sender, size, round(size * 100 / maxSizeGb, 2)
            )
        )


def getBackupsSizeGb():
    dirname = os.path.dirname(__file__)
    backupsDir = str(Path(__file__).parent / "backups")
    filename = os.path.join(dirname, "config.toml")
    configFile = open(filename, "r")
    configData = toml.load(configFile)
    maxSizeGb = float(configData.get("Management").get("MAX_SIZE_GB"))
    size = calcular_directorio(backupsDir)
    return round(size / 2**30, 2), maxSizeGb


def listBackups():
    currentBackups = "No hay copias de seguridad actualmente"
    backupsPath = str(Path(__file__).parent / "backups")
    perday = getBackupsMap()
    if len(perday.keys()) > 0:
        currentBackups = "Las copias de seguridad actuales son:\n"
        for date in sorted(
            perday.keys(),
            key=lambda fecha: datetime.datetime.strptime(fecha, "%d/%m/%Y"),
        ):
            currentBackups += "<em>" + date + "</em> -> \n"
            for bkp in perday[date]:
                currentBackups += "\t<code>" + bkp + "</code>\n"
        size, maxSizeGb = getBackupsSizeGb()
        currentBackups += "{} GB, {}%".format(size, round(size * 100 / maxSizeGb, 2))
    path = str(Path(__file__).parent / "sender.py")
    os.system("python3 " + path + ' "' + currentBackups + '"')


def getBackupsMap(): # ToDo return ordered
    backupsPath = str(Path(__file__).parent / "backups")
    perday = {}
    if os.path.exists(backupsPath) and os.path.isdir(backupsPath):
        currentBackupsList = os.listdir(backupsPath)
        if len(currentBackupsList) > 0:
            for bkp in currentBackupsList:
                day, month, year = bkp[1:].lstrip("backup-").split("-")[0].split(".")
                name = day + "/" + month + "/" + year
                if not name in perday:
                    perday[name] = [bkp]
                else:
                    perday[name].append(bkp)
    for k in perday.keys():
        perday[k] = sorted(
        list(perday.get(k)),
        key=lambda fecha: datetime.datetime.strptime(fecha.split("-")[2].rstrip(".e"), "%H.%M.%S"))
    return perday


def getCompleteBackupsMap(): # ToDo return ordered
    backupsPath = str(Path(__file__).parent / "backups")
    perday = {}
    if os.path.exists(backupsPath) and os.path.isdir(backupsPath):
        currentBackupsList = os.listdir(backupsPath)
        if len(currentBackupsList) > 0:
            for bkp in currentBackupsList:
                if not bkp.startswith("b"):
                    day, month, year = (
                        bkp[1:].lstrip("backup-").split("-")[0].split(".")
                    )
                    name = day + "/" + month + "/" + year
                    if not name in perday:
                        perday[name] = [bkp]
                    else:
                        perday[name].append(bkp)
    for k in perday.keys():
        perday[k] = sorted(
        list(perday.get(k)),
        key=lambda fecha: datetime.datetime.strptime(fecha.split("-")[2].rstrip(".e"), "%H.%M.%S"))
    return perday


def restore(file, omit_not=False):
    if not file.endswith(".e"):
        file += ".e"
    file_route = str(Path(__file__).parent / "backups" / file)
    if os.path.exists(file_route) and not os.path.isdir(file_route):
        if not file.startswith("b"):
            # print(file)
            decompress(file)
            day, month, year = (
                file.lstrip(str(Path(__file__).parent / "backups"))
                .split("-")[1]
                .split(".")
            )
            sender = str(Path(__file__).parent / "sender.py")
            if not omit_not:
                os.system(
                    'python3 {} "Se ha restaurado el sistema con una copia de seguridad del {}/{}/{}: ({})"'.format(
                        sender, day, month, year, file
                    )
                )
        else:
            junkDate = (
                file.lstrip(str(Path(__file__).parent / "backups"))
                .lstrip("backup-")
                .rstrip(".e")
            )
            day, month, year = junkDate.split("-")[0].split(".")
            hour, minute, second = junkDate.split("-")[1].split(".")
            maxDate = datetime.datetime(day=int(day), month=int(month), year=int(year), hour=int(hour), minute=int(minute), second=int(second))
            backupsMap = getCompleteBackupsMap()
            lastCompleteBackup = getLastCompleteBackupList(backupsMap, maxDate)[-1]
            restore(lastCompleteBackup[-1], True)
            decompress(file)
            sender = str(Path(__file__).parent / "sender.py")
            if not omit_not:
                os.system(
                    'python3 {} "Se ha restaurado el sistema con una copia de seguridad del {}/{}/{}: ({})"'.format(
                        sender, day, month, year, file
                    )
                )
        return True
    else:
        return False


def decompress(file):
    file = str(Path(__file__).parent / "backups" / file)
    cypher = str(Path(__file__).parent / "cypher.py")
    os.system("python3 {} d {}".format(cypher, file))
    file = file.rstrip(".e") + ".tar"
    snarFile = str(Path(__file__).parent / "backup.snar")
    os.system(
        "tar --extract --listed-incremental={} --file={} -C/".format(snarFile, file)
    )

    os.system("python3 {} e {} ".format(cypher, file))


'''def getLastCompleteBackupList(backupMap):
    # ToDo MaxDate
    return sorted(
        list(backupMap.keys()),
        key=lambda fecha: datetime.datetime.strptime(fecha, "%d/%m/%Y"),
    )'''

def getLastCompleteBackupList(backupMap, maxDate):
    filtered_dates = []
    for date, files in backupMap.items():
        for file in files:
            if datetime.datetime.strptime(file[1:].rstrip(".e").lstrip("backup-"), "%d.%m.%Y-%H.%M.%S") < maxDate:
                filtered_dates.append(file)
    # filtered_dates = [date for date, file in backupMap.items() if datetime.datetime.strptime(file.rstrip(".e").lstrip("backup-"), "%d.%m.%Y-%H.%M.%S") <= maxDate]
    sorted_dates = sorted(filtered_dates, key=lambda file: datetime.datetime.strptime(file[1:].rstrip(".e").lstrip("backup-"), "%d.%m.%Y-%H.%M.%S"))
    return sorted_dates

def getLastCompleteFilteredBackupList(backupMap):
    sortedYKeys = sortedMKeys = sortedWKeys = None
    for type in ["y", "m", "w"]:
        yKeys = [k for k, v in backupMap.items() for bk in v if bk.startswith(type)]
        if type == "y":
            sortedYKeys = sorted(
                yKeys, key=lambda fecha: datetime.datetime.strptime(fecha, "%d/%m/%Y")
            )
        elif type == "m":
            sortedMKeys = sorted(
                yKeys, key=lambda fecha: datetime.datetime.strptime(fecha, "%d/%m/%Y")
            )
        else:
            sortedWKeys = sorted(
                yKeys, key=lambda fecha: datetime.datetime.strptime(fecha, "%d/%m/%Y")
            )
    return sortedYKeys, sortedMKeys, sortedWKeys


def calcular_directorio(directorio):  # get size in bytes
    return sum(
        [
            sum([os.path.getsize(rutas + "/" + archivo) for archivo in archivos])
            for rutas, _, archivos in os.walk(directorio)
        ]
    )


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "r" and len(sys.argv) == 3:
            restore(sys.argv[2])
        elif sys.argv[1] == "b":
            dobackup()
