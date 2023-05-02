import datetime
import os
import random
from pathlib import Path

filename_pattern = "backup-*-*.e"
yfilename_pattern = "ybackup-*-*.e"
wfilename_pattern = "wbackup-*-*.e"
mfilename_pattern = "mbackup-*-*.e"
dir_path = str(Path(__file__).parent / "backups")
files_to_generate = set()

for year in range(2021, 2024):
    for month in range(1, 13):
        for day in range(1, 29):
            luck = bool(random.getrandbits(1)) and bool(random.getrandbits(1)) and bool(random.getrandbits(1)) and bool(random.getrandbits(1)) and bool(random.getrandbits(1)) and bool(random.getrandbits(1))
            if luck:
                print("Generated date-> " + str(datetime.datetime.strptime("{}/{}/{}".format(day, month, year), "%d/%m/%Y")))
                filename = "backup-{:02}.{:02}.{:02}-{:02}.{:02}.{:02}.e".format(day, month, year, 00, 00, 00)
                filename2 = "wbackup-{:02}.{:02}.{:02}-{:02}.{:02}.{:02}.e".format(day, month, year, 00, 00, 00)
                files_to_generate.add(filename)
                files_to_generate.add(filename2)
                # os.system("touch {}/{}".format(dir_path, filename))
        print("Generated date-> " + str(datetime.datetime.strptime("{}/{}/{}".format("5", month, year), "%d/%m/%Y")))
        filename = "mbackup-{:02}.{:02}.{:02}-{:02}.{:02}.{:02}.e".format(1, month, year, 00, 00, 00)
        files_to_generate.add(filename)
        # os.system("touch {}/{}".format(dir_path, filename))
    print("Generated date-> " + str(datetime.datetime.strptime("{}/{}/{}".format(1, 1, year), "%d/%m/%Y")))
    filename = "ybackup-{:02}.{:02}.{:02}-{:02}.{:02}.{:02}.e".format(1, 1, year, 00, 00, 00)
    files_to_generate.add(filename)
    # os.system("touch {}/{}".format(dir_path, filename))

now = datetime.datetime.now()
for file in files_to_generate:
    if datetime.datetime.strptime(file.split("-")[1], "%d.%m.%Y") < now:
        os.system("touch {}/{}".format(dir_path, file))
