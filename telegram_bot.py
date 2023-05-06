import threading
import telebot
import socket
import backup
import toml
import os


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "config.toml")
try:
    configFile = open(filename, "r")
    configData = toml.load(configFile)
    configFile.close()
    token = configData.get("Telegram").get("API_TOKEN")
except FileNotFoundError:
    configFile = open(os.path.join(dirname, "API_TOKEN.txt"), "r")
    token = configFile.readline().strip("\n")
    configFile.close()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["help", "ayuda"])
def enviar(message):
    if isAuthUser(message.chat.id):
        bot.send_message(
            message.chat.id,
            "Hola "
            + str(message.chat.first_name)
            + ", los comandos que puedes usar son:"
            "\n-/empezar para empezar"
            "\n-/usuarios para conocer el número de usuarios autorizados"
            "\n-/ayuda para ayuda"
            "\n-/backup para hacer una copia de seguridad."
            "\n-/ls para listar las copias de seguridad actuales"
            "\n-/rs [file.e] para restaurar una copia",
        )
    else:
        bot.send_message(
            message.chat.id,
            "Hola "
            + str(message.chat.first_name)
            + ", los comandos que puedes usar son:\n-/empezar para empezar\n-/ayuda para ayuda.\nContacta con el administrador para más información",
        )


@bot.message_handler(commands=["start", "empezar"])
def enviar(message):
    bot.send_message(
        message.chat.id,
        "Hola "
        + str(message.chat.first_name)
        + ", tu id de usuario es: <code>"
        + str(message.chat.id)
        + "</code>. Contacta con el administrador para más información.",
        parse_mode="html",
    )
    notify_user_addition(message.chat.first_name, str(message.chat.id))


@bot.message_handler(commands=["users", "usuarios"])
def getUsers(message):
    id = message.chat.id
    if isAuthUser(id):
        bot.send_message(
            id,
            generateAuthUsersString()
            + "Hola "
            + str(message.chat.first_name)
            + ", el número de usuarios que reciben notificaciones del bot es "
            + str(len(getAuthUsersId()))
            + ": \n<code>"
            + str(getAuthUsersName())
            + "</code>",
            parse_mode="html",
        )
    else:
        bot.send_message(id, generateNoAuthUsersString())


@bot.message_handler(
    commands=[
        "backup",
        "dobackup",
        "doabackup",
        "copiadeseguridad",
        "hazcopiadeseguridad",
        "hazunacopiadeseguridad",
    ]
)
def dobackup(message):
    id = message.chat.id
    if isAuthUser(id):
        backup.dobackup()
    else:
        bot.send_message(id, generateNoAuthUsersString())


@bot.message_handler(
    commands=["ls", "lsbackup", "lsbackups", "listar", "listarbackup", "listarbackups"]
)
def dobackup(message):
    id = message.chat.id
    if isAuthUser(id):
        backup.listBackups()
    else:
        bot.send_message(id, generateNoAuthUsersString())


@bot.message_handler(commands=["rs", "restore", "back", "volver"])
def restore(message):
    id = message.chat.id
    if isAuthUser(id):
        com = str(message.text).split(" ")
        if not len(com) == 2:
            # print(str(com))
            bot.send_message(
                id, "La sintaxis del mensaje es incorrecta:\n\t/rs [fichero.e]"
            )
        else:
            if not backup.restore(com[1]):
                bot.send_message(id, "La copia de seguridad solicitada no existe. Revisa el listado de copias disponible con /ls o el listado completo de comandos con /ayuda.")
    else:
        bot.send_message(id, generateNoAuthUsersString())


def notify_user_addition(name, id):
    for user in getAuthUsersId():
        bot.send_message(
            user,
            generateAuthUsersString()
            + "Usuario "
            + name
            + " con id: "
            + id
            + " acaba de lanzar el bot.",
            parse_mode="html",
        )


def make_communication(text):
    for user in getAuthUsersId():
        bot.send_message(user, generateAuthUsersString() + text, parse_mode="html")


def generateAuthUsersString():
    return "<b>Mensaje para usuarios autorizados</b>\n"


def generateNoAuthUsersString():
    return "No eres un usuario autorizado para esta acción. Avisa al administrador del sistema."


def isAuthUser(userId):
    u = getAuthUsersId()
    if len(u) > 0 and str(userId) in u:
        return True
    return False


def getAuthUsersId():
    return getAuthUsers()[0]


def getAuthUsersName():
    return getAuthUsers()[1]


def getAuthUsers():
    filename = os.path.join(dirname, "auth_users")
    try:
        f = open(filename, "r")
        id = []
        name = []
        for user in f.readlines():
            l = user.split("#")
            if len(l) == 2 and not l[0].strip(" ").startswith("//"):
                id.append(str(l[0]).strip(" "))
                name.append(str(l[1]).strip("\n").strip(" "))
        return id, name
    except FileNotFoundError:
        return [], []


def httpServer():
    host = socket.gethostname()
    port = 5020

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen()
    while True:
        con, address = server_socket.accept()
        data = con.recv(128).decode()
        buf_size = int(data)
        print("recibido: " + str(buf_size))
        con.send("200".encode())
        print("enviado ack")
        data = con.recv(buf_size).decode()
        print("recibido: " + data)
        make_communication(data)
        print("enviado ack2")
        con.send("200".encode())
        con.close()


def answerTelegramMessages():
    try:
        threading.Thread(
            target=bot.infinity_polling, name="bot_infinity_polling", daemon=True
        ).start()
    except TimeoutError:
        print("Falló la conexión, pero se intentará reconectar")
        answerTelegramMessages()


if __name__ == "__main__":
    answerTelegramMessages()
    httpServer()
