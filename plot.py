import sys
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd
import random
import csv

# Get genre for each song
genre_lookup = {}
with open('csv/liked.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
                song, artist, genre = row[1], row[3], row[19].split(',')[0].split(' ')[-1]
                key = f'{artist} | {song}'
                genre_lookup[key] = genre

# Read data
paths = sys.argv[1:]

data = {}
for path in paths:
        print(path)
        data[path] = {}
        
        with open(path) as f:
                lines = f.read().split('\n')
                for line in lines:
                        chunks = line.split(': ')
                        if len(chunks) == 2:
                                data[path][chunks[0]] = chunks[1]
                                
paths = []
qualitys = []
valences = []
intensitys = []
genres = []
artists = []
song_names = []

for (path, props) in data.items():
        keys = props.keys()
        if 'quality' in keys and 'valence' in keys and 'intensity' in keys:
                print(path)
                print('\tquality:', props['quality'])
                print('\tvalence:', props['valence'])
                print('\tintensity:', props['intensity'])
                
                paths.append(path)
                q, v, i = float(props['quality']) + random.randint(-10, 10) / 20, \
                        float(props['valence']) + random.randint(-10, 10) / 20, \
                        float(props['intensity']) + random.randint(-10, 10) / 20
                qualitys.append(q)
                valences.append(v)
                intensitys.append(i)

                artist, song_name = path.split('/')[-1].split(' | ')
                song_names.append(song_name)
                artists.append(artist)

                genre_key = f'{artist} | {song_name}'
                if genre_key in genre_lookup.keys():
                        genre = genre_lookup[genre_key]
                else:
                        genre = ''
                genres.append(genre)

print(f'{len(paths)} songs have all 3 properties.')

df = pd.DataFrame(data={
        'quality': qualitys,
        'valence': valences,
        'intensity': intensitys,
        'color': genres,
        'artist': artists,
        'song_name': song_names
})
assert(len(qualitys) == len(valences) == len(intensitys))
fig = px.scatter_3d(df, x='quality', y='valence', z='intensity', color='color', hover_data=['artist', 'song_name'])
fig.show()
