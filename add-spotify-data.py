'''
Adds a variety of data like danceability and energy from a Spotify-exported CSV.
'''

import sys
import csv
import pprint
import yaml
import common

if len(sys.argv) != 3:
        print('Usage: add-spotify-data.py CSVFILE OUTDIR')
        sys.exit(1)

in_path, out_dir = sys.argv[1], sys.argv[2]

# Strip trailing / on out_dir
if out_dir[-1] == '/':
        out_dir = out_dir[:-1]

columns = {
        'Track URI': 0,
        'Artist URI(s)': 2,
        'Album URI': 4,
        'Album Name': 5,
        'Album Release Date': 8,
        'Album Image URL': 9,
        'Track Number': 11,
        'Track Duration (ms)': 12,
        'Explicit': 14,
        'Popularity': 15,
        'Artist Genres': 19,
        'Danceability': 20,
        'Energy': 21,
        'Key': 22,
        'Loudness': 23,
        'Mode': 24,
        'Speechiness': 25,
        'Acousticness': 26,
        'Instrumentalness': 27,
        'Liveness': 28,
        'Valence': 29,
        'Tempo': 30,
        'Time Signature': 31,
        'Album Genres': 32,
        'Label': 33
}

with open(in_path) as csvfile:
        reader = csv.reader(csvfile)

        # Skip header
        next(reader)

        for row in reader:
                song, artist = row[1], row[3]

                song_path = f'{out_dir}/{common.song_path(song, artist)}'

                # Read into data dict
                data = {}
                for (key, idx) in columns.items():
                        value = row[idx]
                        if ',' in value: value = value.split(',')
                        if value == '': continue

                        try: value = float(value)
                        except (ValueError, TypeError): pass

                        data[key] = value

                print(f'{song} | {artist}')
                pprint.pprint(data)

                # Now actually write
                with open(song_path, 'a') as out_file:
                        yaml.dump(data, stream=out_file)

    
