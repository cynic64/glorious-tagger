import csv
import sys
import os

if len(sys.argv) < 2:
	print('Usage: download.py FILE')
	sys.exit(1)

path = sys.argv[1]

with open(path) as csvfile:
	reader = csv.reader(csvfile)

	next(reader)
	for row in reader:
		artist, song, id = row[3], row[1], row[0].split(':')[-1]

		command = f'ytmdl "{song}" --artist "{artist}" --choice 1 --quiet --trim --spotify-id "{id}"'
		print('Command: ', command)
		os.system(command)
