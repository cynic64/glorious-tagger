import csv
import sys
import os

if len(sys.argv) != 3:
        print('Usage: dl-covers.py FILE OUT_DIR')
        sys.exit(1)

path = sys.argv[1]
out_dir = sys.argv[2]
with open(path) as csvfile:
        reader = csv.reader(csvfile)

        # Skip headers
        next(reader)
        for row in reader:
                song, artist, cover =  row[1], row[3], row[9]
                path = f'{out_dir}/{artist} | {song}.jpg'
                command = f'wget "{cover}" -O "{path}"'
                print(command)
                os.system(command)
