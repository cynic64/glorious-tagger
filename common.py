SPOTIFY_URL = 'https://api.spotify.com/v1'

def song_path(song, artist):
        artist = artist.replace('|', '')
        artist = artist.replace('\n', '')
        artist = artist.replace('/', '%')
        song = song.replace('|', '')
        song = song.replace('\n', '')
        song = song.replace('/', '%')

        return f'{artist} | {song}'
