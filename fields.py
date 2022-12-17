import csv
import sys

if len(sys.argv) < 3:
	print('Usage: fields.py FILE COLUMNS')
	sys.exit(1)

path, columns = sys.argv[1], [int(x) for x in sys.argv[2:]]

with open(path) as csvfile:
	reader = csv.reader(csvfile)

	for row in reader:
		print(' ||| '.join([row[i] for i in columns]))
