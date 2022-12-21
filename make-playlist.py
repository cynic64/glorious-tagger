import auth
import requests
import pprint
import json
from common import SPOTIFY_URL
import sys
import yaml

if len(sys.argv) < 2:
        print('Usage: make-playlist.py FILES')
        sys.exit(1)

access_token, user_id, headers = auth.authorize('playlist-modify-public')

# Create playlist
response = requests.post(f'{SPOTIFY_URL}/users/{user_id}/playlists',
                         headers=headers,
                         json={
                                 'name': 'Generated playlist',
                                 'description': 'Generated by Lord Nicky\'s https://github.com/cynic64/glorious-tagger'
                         })

assert(response.status_code == 201)
playlist_id = json.loads(response.content)['id']
print('New playlist has id:', playlist_id)

# Now add songs
songs = []
for path in sys.argv[1:]:
        with open(path) as f:
                data = yaml.safe_load(f)

        if data == None: continue

        if 'Track URI' in data.keys() and 'quality' in data.keys():
                quality, uri = data['quality'], data['Track URI']
                if quality < 9: continue

                data['path'] = path
                songs.append(data)


# Sort by ascending intensity
songs = sorted(songs, key=lambda song: song['valence'])
songs = list(reversed(songs))
pprint.pprint([song['path'] for song in songs])

print(f'Will add {len(songs)} tracks')

# Spotify limits us to adding 100 songs at once
uris = [song['Track URI'] for song in songs]
limit = 100
for offset in range(0, len(uris), 100):
        chunk = uris[offset:offset+100]
        print(f'Adding {len(chunk)} items starting at offset {offset}')
        response = requests.post(f'{SPOTIFY_URL}/playlists/{playlist_id}/tracks',
                                headers=headers,
                                json={
                                        'uris': chunk,
                                        'position': offset
                                })

        assert(response.status_code == 201)
