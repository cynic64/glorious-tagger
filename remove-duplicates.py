'''
Removes duplicate entries from database.
'''

import sys
import yaml
import pprint

if len(sys.argv) < 2:
        print('Usage: remove-dupliciates.py FILES')
        sys.exit(1)

for path in sys.argv[1:]:
        print(f'Processing {path}')
        with open(path) as in_file:
                text = in_file.read()

        data = yaml.safe_load(text)
        with open(path, 'w') as out_file:
                yaml.dump(data, out_file)
