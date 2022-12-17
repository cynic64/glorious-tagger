import csv
import sys
import os

if len(sys.argv) != 3:
	print('Usage: csv-to-db.py INPUT OUTPUT')
	sys.exit(1)

in_path, out_path = sys.argv[1], sys.argv[2]

with open(in_path, 'r') as csvfile, open(out_path, 'w') as outfile:
	reader = csv.reader(csvfile)

	next(reader)
	for row in reader:
		artist, song = row[3], row[1]
		artist = artist.replace('|', '')
		artist = artist.replace('\n', '')
		artist = artist.replace('/', '%')
		song = song.replace('|', '')
		song = song.replace('\n', '')
		song = song.replace('/', '%')

		outfile.write(f'{artist} | {song}\n')
