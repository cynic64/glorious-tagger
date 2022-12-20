import requests
import hashlib
import base64
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import pprint
import json

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
                pprint.pprint(form)
                self.server.code = form['code']

# Stole this from spotipy too >:)
def get_code_verifier():
        """ Spotify PCKE code verifier - See step 1 of the reference guide below
        Reference:
        """
        # Range (33,96) is used to select between 44-128 base64 characters for the
        # next operation. The range looks weird because base64 is 6 bytes
        import random
        length = random.randint(33, 96)

        # The seeded length generates between a 44 and 128 base64 characters encoded string
        import secrets
        verifier = secrets.token_urlsafe(length)
        return verifier

def get_code_challenge():
        verifier = get_code_verifier()
        code_challenge_digest = hashlib.sha256(verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge_digest).decode('utf-8')
        code_challenge = code_challenge.replace('=', '')

        return (code_challenge, verifier)

# First get the authorization code
(code_challenge, code_verifier) = get_code_challenge()
payload = {
        'client_id': 'b588d0ec58d346899744fb573f271d0c',
        'response_type': 'code',
        'redirect_uri': 'http://localhost:8080',
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge,
}

url_params = urllib.parse.urlencode(payload)
url = f'https://accounts.spotify.com/authorize?{url_params}'
print('Code challenge:', code_challenge)
print('URL to open:', url)

server = HTTPServer(("localhost", 8080), RequestHandler)
server.handle_request()

assert(server.code != None)

print('Using code:', server.code)

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

print(response.status_code)

response_string = urllib.parse.urlparse(response.content).path
token = json.loads(response_string)['access_token']
print('Token:', token)
