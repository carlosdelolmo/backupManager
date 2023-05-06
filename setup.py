import os
import random
import string
from pathlib import Path
from sys import argv

from crontab import CronTab
import toml


def getUsuarios():
    x = 0
    res = "//  Syntax help\n//\n//  Use '//' to comment line\n//  Use '#' as separator between id and name\n//\n// id # name\n"
    nextUid = input(
        "Introduce el UID del usuario {} o pulsa intro para terminar: ".format(x)
    )
    while len(nextUid) > 0:
        nextUsername = input("Introduce un apodo para el usuario {}: ".format(x))
        if len(nextUsername) > 0:
            res += nextUid + " # " + nextUsername + "\n"
            print(
                "Guardado usuario {} -> UID:{}; Apodo:{}\n".format(
                    x, nextUid, nextUsername
                )
            )
            x += 1
            nextUid = input(
                "Introduce el UID del usuario {} o pulsa intro para terminar: ".format(
                    x
                )
            )
        else:
            break
    with open("auth_users", "w") as f:
        f.write(res)
    return res


def getDirectorios():
    x = 0
    res = "//  Syntax help\n//\n//  Use '//' to comment line\n//\n// absolute path of files or folders to backup\n//\n"
    nextPath = input(
        "Introduce el Path absoluto del fichero {} a respladar o pulsa intro para terminar: ".format(
            x
        )
    )
    while len(nextPath) > 0:
        if nextPath.startswith("/"):
            res += nextPath + "\n"
            print("Guardado fichero {} -> Path:{}\n".format(x, nextPath))
            x += 1
            nextPath = input(
                "Introduce el Path absoluto del fichero {} a respladar o pulsa intro para terminar: ".format(
                    x
                )
            )
        else:
            nextPath = input(
                "Por favor, introduce el path ABSOLUTO del fichero {} a respaldar o pulsa intro para terminar: ".format(
                    x
                )
            )
            if len(nextPath) == 0:
                break
    with open("backup_files", "w") as f:
        f.write(res)
    return res


def getToml():
    with open("API_TOKEN.txt", "r") as f:
        apiToken = f.readline().strip(" \n")
    path = str(Path(__file__).parent / "API_TOKEN.txt")
    os.system("rm {}".format(path))
    maxSizeGb = float(
        input(
            "Por favor, introduce el tamaño máximo que puede ocupar el directorio de backups, en GB: "
        )
    )
    while not (len(str(maxSizeGb)) > 0):
        maxSizeGb = float(
            input(
                "Por favor, introduce el tamaño máximo que puede ocupar el directorio de backups, en GB: "
            )
        )

    print("Guardado tamaño máximo: {} GB\n".format(maxSizeGb))
    cypherPass = input("Por favor, introduce la contraseña de cifrado de las copias: ")
    while not (len(apiToken) > 0):
        cypherPass = input(
            "Por favor, introduce la contraseña de cifrado de las copias: "
        )
    print("Guardada contraseña de cifrado\n")
    key_pass = "".join(random.choices(string.ascii_letters + string.digits, k=15))

    res = {
        "Telegram": {"API_TOKEN": "{}".format(apiToken)},
        "Cypher": {"PASSWORD": "{}".format(key_pass)},
        "Management": {"MAX_SIZE_GB": maxSizeGb},
    }

    with open("config.toml", "w") as f:
        toml.dump(res, f)

    generate_key(cypherPass, key_pass)
    return res


def generate_key(backup_pass, key_file_pass):
    keypath = str(Path(__file__).parent / ".key")
    os.system("echo {} > {}".format(backup_pass, keypath))
    encrypt(keypath, key_file_pass, "")


def encrypt(file, password, ext):
    bash_command = "openssl aes-256-cbc -in {} -k {} -pbkdf2 -out {}".format(
        file, password, file.rstrip(ext) + ".e"
    )
    bash_command += "; rm -f {}".format(file)
    os.system(bash_command)
    os.system("chmod 1441 {}".format(file.rstrip(ext) + ".e"))


def buildCrontab():
    user = os.environ.get("USER")
    cron = CronTab(user=True)

    job1 = cron.new(
        command="/usr/bin/python3 /home/{}/backupManager/telegram_bot.py".format(user)
    )
    job1.setall("@reboot")

    job2 = cron.new(
        command="/usr/bin/python3 /home/{}/backupManager/backup.py b".format(user)
    )
    job2.setall("59 23 * * *")

    cron.write()


if __name__ == "__main__":
    getUsuarios()
    getDirectorios()
    getToml()
    buildCrontab()
    os.remove(argv[0])
