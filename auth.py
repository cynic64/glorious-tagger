import requests
import hashlib
import base64
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import pprint
import json
import webbrowser
from common import SPOTIFY_URL

CLIENT_ID = 'b588d0ec58d346899744fb573f271d0c'
CACHE_PATH = 'token_cache'

# Stole this from spotipy
class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
                self.send_response(200)
                self.send_header("Content_Type", "text/html")
                self.end_headers()

                self.wfile.write('''<html>
                <script>
                window.close()
                </script>
                <body>
                <h1>No idea what happened bro</h1>
                <script>
                window.close()
                </script>
                <button class="closeButton" style="cursor: pointer" onclick="window.close();">Close Window</button>
                </body>
                </html>'''.encode('utf-8'))

                query_string = urllib.parse.urlparse(self.path).query
                form = dict(urllib.parse.parse_qsl(query_string))
                self.server.code = form['code']

# Stole this from spotipy too >:)
def get_code_verifier():
        # Range (33,96) is used to select between 44-128 base64 characters for the
        # next operation. The range looks weird because base64 is 6 bytes
        import random
        length = random.randint(33, 96)

        # The seeded length generates between a 44 and 128 base64 characters encoded string
        import secrets
        verifier = secrets.token_urlsafe(length)
        return verifier

# And this too, mostly
def get_code_challenge():
        verifier = get_code_verifier()
        code_challenge_digest = hashlib.sha256(verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge_digest).decode('utf-8')
        code_challenge = code_challenge.replace('=', '')

        return (code_challenge, verifier)

# But the rest is mine!
def get_auth_tokens_from_scratch(scope):
        '''
        This forces the user to authenticate. Try loading cached refresh_token first.
        '''
        # First get the authorization code
        code_challenge, code_verifier = get_code_challenge()
        payload = {
                'client_id': CLIENT_ID,
                'response_type': 'code',
                'redirect_uri': 'http://localhost:8080',
                'scope': scope,
                'code_challenge_method': 'S256',
                'code_challenge': code_challenge,
        }

        # Get URL for the user to authorize with
        url_params = urllib.parse.urlencode(payload)
        url = f'https://accounts.spotify.com/authorize?{url_params}'

        webbrowser.open_new_tab(url)

        server = HTTPServer(("localhost", 8080), RequestHandler)
        server.handle_request()

        assert(server.code != None)

        # Then request the access token
        response = requests.post('https://accounts.spotify.com/api/token', {
                'grant_type': 'authorization_code',
                'code': server.code,
                'redirect_uri': 'http://localhost:8080',
                'client_id': 'b588d0ec58d346899744fb573f271d0c',
                'code_verifier': code_verifier
        }, headers={
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        })

        assert(response.status_code == 200)

        response_json = json.loads(response.content)
        return response_json['access_token'], response_json['refresh_token']

def get_auth_tokens_from_cache(scope):
        '''
        scope is needed to check whether the cached tokens provide access to the same scope.
        Returns None on failure.
        '''
        try: f = open(CACHE_PATH)
        except FileNotFoundError: return

        with f:
                j = json.load(f)
                old_access_token, old_refresh_token = j['access_token'], j['refresh_token']

                old_scope = j['scope']
                if old_scope != scope:
                        print(f'Cached tokens have different scope {old_scope} vs. {scope}.')
                        print('Can\'t use cached tokens.')
                        return

                response = requests.post('https://accounts.spotify.com/api/token',
                                        data={
                                                'grant_type': 'refresh_token',
                                                'refresh_token': old_refresh_token,
                                                'client_id': CLIENT_ID
                                        },
                                        headers={
                                                'Content-Type': 'application/x-www-form-urlencoded',
                                        })

                if response.status_code != 200:
                        print('Failed to use cached tokens. Status:', status)
                        return

                response_json = json.loads(response.content)
                return response_json['access_token'], response_json['refresh_token']

def store_tokens(access_token, refresh_token, scope):
        with open(CACHE_PATH, 'w') as f:
                json.dump({
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'scope': scope,
                }, f)

def authorize(scope):
        '''
        First tries using cached token, then falls back on making user authenticate.

        scope should be a space-separated string of the scopes you want access to.

        Returns access_token, user_id, headers.
        '''
        # First try to use cached tokens
        tokens = get_auth_tokens_from_cache(scope)

        if tokens: access_token, refresh_token = tokens
        # Didn't work, ask user
        else: access_token, refresh_token = get_auth_tokens_from_scratch(scope)

        store_tokens(access_token, refresh_token, scope)

        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
        }

        # Get user ID
        response = requests.get(f'{SPOTIFY_URL}/me',
                                headers=headers)

        assert(response.status_code == 200)
        user_id = json.loads(response.content)['id']

        return access_token, user_id, headers
