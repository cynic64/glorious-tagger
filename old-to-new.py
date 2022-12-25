'''
Converts my old format of many individual files to the new, Glorious Single File Format™
'''

import sys
import pprint
import yaml
import common

if len(sys.argv) < 3:
        print('Usage: old_to_new.py OUTPUT IN1 IN2 IN3...')
        sys.exit(1)

out_path = sys.argv[1]
in_paths = sys.argv[2:]
print(out_path)

tracks = {}

for in_path in in_paths:
        print(f'Loading {in_path}')
        track_name = in_path.split('/')[-1]
        assert(track_name not in tracks.keys())

        with open(in_path, 'r') as f:
                tracks[track_name] = yaml.safe_load(f)

# Make lists comma-separated
for (track_name, track_data) in tracks.items():
        for (key, value) in track_data.items():
                while type(value) == list:
                        value = ', '.join(value)
                tracks[track_name][key] = value

print(f'Dumping {len(tracks)} tracks...')

with open(out_path, 'w') as f:
        common.store(f, tracks)
