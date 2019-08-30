import requests
from bs4 import BeautifulSoup
import base64
import json
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--settings',
                    help='settings file', default='settings.json')
parser.add_argument('-c', '--create',
                    action='store_true',
                    help='create playlist')
args = parser.parse_args()

with open(args.settings) as settings_file:
    settings = json.load(settings_file)

user = settings['user']
client_id = settings['client_id']
client_secret = settings['client_secret']
refresh_token = settings['refresh_token']
playlist_id = settings.get('playlist_id')

# Get playlist tracks.

page = requests.get('https://www.bbc.co.uk/sounds/play/p07lc3pw')

soup = BeautifulSoup(page.text, 'html.parser')

scripts = soup.find_all('script')

for script in scripts:
    script_src = script.text
    if 'spotify' not in script_src:
        continue
    script_start_indx = script_src.find('{')
    script_end_indx = script_src.rfind('}')
    script_json = json.loads(script_src[script_start_indx:script_end_indx+1])
    break

availability = script_json['programmes']['current']['availability']
week_starting = availability['from']
tracks = script_json['tracklist']['tracks']

# Transform tracks to spotify URIs.

spotify_uris = []
for track in tracks:
    track_uris = track['uris']
    for track_uri in track_uris:
        if track_uri['label'] == 'Spotify':
            spotify_uris.append(track_uri['uri'])

spotify_tracks = [ 'spotify:track:' + spotify_uri.split('/')[-1]
                   for spotify_uri in spotify_uris ]

# Get authorization token.

client_id_secret_base64 = base64.b64encode(
    (client_id + ':' + client_secret).encode()).decode('ascii')

headers = {
    'Authorization': 'Basic ' + client_id_secret_base64
}

payload = {
    'grant_type' : 'refresh_token',
    'refresh_token': refresh_token
}

r = requests.post('https://accounts.spotify.com/api/token',
                  data=payload,
                  headers=headers)

response = r.json()

if r.status_code != 200:
    print('Error refreshing token.')
    print(r.json()['error'])
    sys.exit(1)

access_token = response['access_token']

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

if args.create: # Create list.

    payload = {
        'name': 'Transcribed BBC Radio 6 Music List',
    }

    r = requests.post(f'https://api.spotify.com/v1/users/{user}/playlists',
                      data=json.dumps(payload),
                      headers=headers)

    response = r.json()

    if r.status_code != 200 and r.status_code != 201:
        print('Error creating playlist.')
        print(response['error'])
        sys.exit(1)

    playlist_id = response['id']
    print(f'Playlist ID: {playlist_id}')

if not playlist_id:
    print('Error finding playlist.')
    print('No playlist ID')
    sys.exit(1)
    
# Populate playlist.
    
payload = {
    'uris': spotify_tracks
}

r = requests.put(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
                 data=json.dumps(payload),
                 headers=headers)

response = r.json()

if r.status_code != 201:
    print('Error populating playlist.')
    print(response['error'])
    sys.exit(1)
    
# Update description.

payload = {
    'description': 'Transcribed BBC Radio 6 Playlist ' + week_starting
}

r = requests.put(f'https://api.spotify.com/v1/playlists/{playlist_id}',
                 data=json.dumps(payload),
                 headers=headers)

if r.status_code != 200:
    print('Error updating playlist description.')
    print(r.json()['error'])
    sys.exit(1)

print('OK')
