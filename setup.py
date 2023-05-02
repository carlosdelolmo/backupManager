import os
import random
import string
from pathlib import Path

import toml


def getUsuarios():
    x = 0
    res = "//  Syntax help\n//\n//  Use '//' to comment line\n//  Use '#' as separator between id and name\n//\n// id # name\n"
    nextUid = input("Introduce el UID del usuario {} o pulsa intro para terminar: ".format(x))
    while(len(nextUid) > 0):
        nextUsername = input("Introduce un apodo para el usuario {}: ".format(x))
        if len(nextUsername) > 0:
            res += nextUid + " # " + nextUsername + "\n"
            print("Guardado usuario {} -> UID:{}; Apodo:{}\n".format(x, nextUid, nextUsername))
            x += 1
            nextUid = input("Introduce el UID del usuario {} o pulsa intro para terminar: ".format(x))
        else:
            break
    with open('notified_users', 'w') as f:
        f.write(res)
    return res

def getDirectorios():
    x = 0
    res = "//  Syntax help\n//\n//  Use '//' to comment line\n//\n// absolute path of files or folders to backup\n//\n"
    nextPath = input("Introduce el Path absoluto del fichero {} a respladar o pulsa intro para terminar: ".format(x))
    while (len(nextPath) > 0):
        if nextPath.startswith("/"):
            res += nextPath + "\n"
            print("Guardado fichero {} -> Path:{}\n".format(x, nextPath))
            x += 1
            nextPath = input("Introduce el Path absoluto del fichero {} a respladar o pulsa intro para terminar: ".format(x))
        else:
            nextPath = input("Por favor, introduce el path ABSOLUTO del fichero {} a respaldar o pulsa intro para terminar: ".format(x))
            if len(nextPath) == 0:
                break
    with open('backup_files', 'w') as f:
        f.write(res)
    return res

def getToml():
    apiToken = input("Por favor, introduce el Token API del bot de Telegram: ")
    while not (len(apiToken) > 0):
        apiToken = input("Por favor, introduce el Token API del bot de Telegram: ")
    maxSizeGb = float(input("Por favor, introduce el tamaño máximo que puede ocupar el directorio de backups, en GB: "))
    while not (len(apiToken) > 0):
        maxSizeGb = float(input("Por favor, introduce el tamaño máximo que puede ocupar el directorio de backups, en GB: "))
    cypherPass = input("Por favor, introduce la contraseña de cifrado de las copias: ")
    while not (len(apiToken) > 0):
        cypherPass = input("Por favor, introduce la contraseña de cifrado de las copias: ")
    key_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    generate_key(cypherPass, key_pass)

    res = {
        'API_TOKEN': '{}'.format(apiToken),
        'Cypher': {
            'PASSWORD': '{}'.format(key_pass)
        },
        'Management': {
            'MAX_SIZE_GB': maxSizeGb
        }
    }

    with open('config.toml', 'w') as f:
        toml.dump(res, f)
        return res

def generate_key(backup_pass, key_file_pass):
    keypath = str(Path(__file__).parent / ".key")
    cypher = str(Path(__file__).parent / "cypher.py")
    os.system("echo {} > {}".format(backup_pass, keypath))
    os.system("python3 {} e {}".format(cypher, keypath))

if __name__ == "__main__":
    getUsuarios()
    getDirectorios()
    getToml()