import sys
import yaml

if len(sys.argv) < 2:
        print('Usage: read.py FILES')
        sys.exit(1)

for path in sys.argv[1:]:
        with open(path) as f:
                try:
                        print(yaml.safe_load(f))
                except yaml.YAMLError as exception:
                        print(exception)
