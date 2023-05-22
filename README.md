
# backupManager


backupManager es un gestor de copias de seguridad cifradas. El sistema está integrado con un bot de Telegram para su gestión remota de forma segura, administradas por uno o más usuarios verificados por el administrador. El proyecto forma parte de un trabajo para la asignatura [EI1056-Seguridad Informática](https://ujiapps.uji.es/sia/rest/publicacion/2022/estudio/225/asignatura/EI1056) del grado de Ingeniería Informática en la Universitat Jaume I.

## Authors

- [@carlosdelolmo](https://github.com/carlosdelolmo)


## Funcionamiento básico
Una vez instalado, el programa se ejecuta automáticamente al iniciar el equipo. Las copias de seguridad se realizan automáticamente cada día, aunque se pueden realizar de forma manual mediante el bot de Telegram. Para que las copias sean automáticas, el equipo debe estar encendido a las 23:59.
## Uso del bot
### Comandos para usuarios sin autenticar
#### /empezar
El bot responde con el UID del usuario.

#### /ayuda
El bot responde con una breve explicación de las funciones que puede realizar el usuario.
### Comandos para usuarios autenticados
Además de todas las funciones que pueden realizar los usuarios sin autenticar, el usuario autenticado podrá usar las siguientes funciones:
#### /ls 
El bot responde con un listado de las copias de seguridad actuales realizadas.
#### /usuarios
El bot responde con un listado de los usuarios autorizados.
#### /backup
El bot realiza una copia de seguridad en ese mismo momento.
#### /rs [nombre_de_la_copia]
El bot restaura el sistema a partir del nombre de la copia de seguridad dada. El nombre se puede obtener a partir del comando */ls*

### Notificaciones del bot
Las notificaciones del bot solo se enviarán a los usuarios autenticados. El bot enviará notificaciones en los siguientes casos:
- Un usuario ejecuta el comando */empezar*. El bot envía un mensaje a todos los usuarios autenticados con el nombre y el UID del usuario que lo invoca.
- Se realiza una copia de seguridad, automática o solicitada mediante bot. El bot envía un mensaje avisando de la realización de la copia.
- Se restaura una copia de seguridad. El bot envía un mensaje avisando de la restauración de la copia.
- Se elimina automáticamente una copia. El bot envía un mensaje avisando de la eliminación de la copia.
- Se supera el 70% del límite de almacenamiento establecido. El bot envía un mensaje avisando del almacenamiento actual del directorio de copias.
## Instalación

Instalación en un equipo Linux basado en Debian

1. Crea tu propio bot de Telegram mediante el [procedimiento habitual](https://core.telegram.org/bots#how-do-i-create-a-bot) y posteriormente mánadale un mensaje cualquiera para guardarlo en tu bandeja de mensajes.

2. Guárdate el Token de tu bot que obtendrás durante la creación, lo necesitarás más adelante.

3. Ejecuta el siguiente código en un terminal bash
```bash
  sudo apt-get update
  sudo apt-get install pip
  sudo apt-get install python3
  sudo apt-get install git
  cd ~
  git clone https://github.com/carlosdelolmo/backupManager.git 
  cd backupManager
  pip install -r requirements.txt
```
4. Introduce el Token de tu bot en el fichero *API_TOKEN.txt*; puedes hacerlo usando el siguiente comando
```bash
  cd ~/backupManager
  echo "Tu_token" > API_TOKEN.txt
```
5. Obtén tu UID de Telegram:

5.1 Ejecuta el siguiente script para obtener tu UID de Telegram con el bot creado anteriormente:
```bash
  cd ~/backupManager
  python3 telegram_bot.py
```
5.2 Envía al bot el siguiente mensaje. Deberá responderte con tu UID. Guárdatelo, lo necesitarás más adelante.
```txt
  /empezar
```
5.3 Puedes parar el bot de Telegram, no lo necesitarás más por ahora. Pulsa *Ctrl + c* sobre la ventana en la que estabas ejecutando el paso 5.1.

6. Configura el gestor de copias según tu necesidad:
6.1 Ejecuta el siguiente script para configurar backupManager a tu gusto 
```bash
  cd ~/backupManager
  python3 setup.py
```
6.1. Deberás introducir tu UID, que deberías tener guardado del paso 5.

6.2. Introduce un apodo para identificar ese usuario. Ahora este usuario estará autenticado, y podrá gestionar el bot y recibir notificaciones de copias de seguridad y restauraciones. Pudes repetir estos dos últimos pasos tantas veces como necesites. Pulsa intro para pasar al siguiente paso.

6.3. Introduce la ruta absoluta del fichero o directorio que quieras respaldar. Pudes repetir este último paso tantas veces como necesites. Pulsa intro para pasar al siguiente paso.

6.4. Introduce en GB el tamaño máximo que pretendas que ocupe el directorio de copias de seguridad. El gestor alertará cuando quede poco para alcanzar ese límite.

6.5. Introduce la contraseña de cifrado de las copias de seguridad.

7. Reinicia el sistema para terminar; puedes usar el siguiente comando.
```bash
  sudo reboot now
```
En caso de querer añadir nuevos ficheros a las copias de seguridad o querer añadir nuevos usuarios autenticados, se pueden modificar en cualquier momento los ficheros *notified_users* y *backup_files*, cuya sintaxis está explicada en el propio fichero.

## Desinstalación
```bash
user=$(whoami)
(crontab -u $user -l | grep -v '/usr/bin/python3 /home/'$user'/backupManager/telegram_bot.py') | crontab -u $user -
(crontab -u $user -l | grep -v '/usr/bin/python3 /home/'$user'/backupManager/backup.py b') | crontab -u $user -
rm -rf ~/backupManager
```

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)

![Logo](https://aulavirtual.uji.es/pluginfile.php/2/core_admin/logocompact/300x300/1684728173/logo_compacto.png)

© 2023 Carlos del Olmo
