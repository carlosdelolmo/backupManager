import os
import sys
import toml


def cypher(file, password, ext):
    bash_command = "openssl aes-256-cbc -in {} -k {} -pbkdf2 -out {}".format(file, password, file.rstrip(ext)+".e")
    bash_command += "; rm -f {}".format(file)
    os.system(bash_command)
    os.system("chmod 1441 {}".format(file.rstrip(ext)+".e"))


def decypher(file, password, ext):
    bash_command = "openssl aes-256-cbc -d -in {} -k {} -pbkdf2 -out {}".format(file, password, file.rstrip(".e")+ext)
    bash_command += "; rm -f {}".format(file)
    os.system(bash_command)


def getpwd(file, upwd):
    decypher(file+".e", upwd, " ")
    fpwd = open(file, "r").readline().strip("\n")
    cypher(file, upwd, " ")
    return fpwd


if __name__ == '__main__':
    # getpwd(".key", "patata123")
    if len(sys.argv) == 3:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'config.toml')
        configFile = open(filename, "r")
        configData = toml.load(configFile)
        upwd = configData.get("Cypher").get("PASSWORD")
        masterpwd = getpwd(os.path.join(dirname, ".key"), upwd)
        # print(masterpwd)
        if sys.argv[1] == 'e':
            cypher(sys.argv[2], masterpwd, ".tar")
        elif sys.argv[1] == 'd':
            decypher(sys.argv[2], masterpwd, ".tar")
