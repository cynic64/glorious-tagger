import sys
import time
import common
import pprint

if len(sys.argv) != 3:
        print('Usage: perf-test.py INPUT OUTPUT')
        sys.exit(1)

in_path, out_path = sys.argv[1], sys.argv[2]

# Load
start = time.time()
with open(in_path, 'r') as f:
        tracks = common.load(f)
end = time.time()
print(f'Loading {len(tracks)} tracks took {end - start}s')

# Store
start = time.time()
with open(out_path, 'w') as f:
        common.store(f, tracks)
end = time.time()
print(f'Storing tracks took {end - start}s')
