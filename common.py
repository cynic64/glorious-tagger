SPOTIFY_URL = 'https://api.spotify.com/v1'

def song_path(song, artist):
        artist = artist.replace('|', '')
        artist = artist.replace('\n', '')
        artist = artist.replace('/', '%')
        song = song.replace('|', '')
        song = song.replace('\n', '')
        song = song.replace('/', '%')

        return f'{artist} | {song}'

def store(stream, tracks):
        '''
        tracks should be a dictionary with keys being track names and values being a dictionary
        of track data.
        '''
        for (track_name, track_data) in tracks.items():
                stream.write(f'---\n{track_name}\n')

                for (key, value) in track_data.items():
                        stream.write(f'{key}: {value}\n')

def load(stream):
        '''
        Returns a dictionary of tracks
        '''
        tracks = stream.read().split('---\n')
        out = {}
        for track in tracks:
                lines = track.split('\n')
                track_name = lines[0]
                out[track_name] = {}
                for item in lines[1:]:
                        if item == '': continue
                        chunks = item.split(': ')
                        key, value = chunks[0], ': '.join(chunks[1:])

                        try: value = float(value)
                        except ValueError: pass

                        out[track_name][key] = value

        return out
