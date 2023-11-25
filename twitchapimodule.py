# Different Functions using the Twitch API specifically. Stuff like getting the Viewer Count.
# Existential for twitchhelper & chatreadingmodule
# Made by iLollek

import requests

def get_viewer_count(username, CLIENT_ID, CLIENT_SECRET):
    # Get OAuth token
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    token = response.json().get('access_token', '')

    # Get stream information
    headers = {'Client-ID': CLIENT_ID, 'Authorization': f'Bearer {token}'}
    url = f'https://api.twitch.tv/helix/streams?user_login={username}'
    response = requests.get(url, headers=headers)
    data = response.json()

    # Extract viewer count from the response
    stream = data.get('data', [])
    viewer_count = stream[0]['viewer_count'] if stream else 0

    return viewer_count

def get_oauth_token(CLIENT_ID, CLIENT_SECRET):
    # Get OAuth token
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    token = response.json().get('access_token', '')
    return token

def get_user_chat_color(user_id, CLIENT_ID, CLIENT_SECRET):

    token = get_oauth_token(CLIENT_ID, CLIENT_SECRET)

    # Get user chat color
    headers = {'Client-ID': CLIENT_ID, 'Authorization': f'Bearer {token}'}
    url = f'https://api.twitch.tv/helix/chat/color?user_id={user_id}'
    response = requests.get(url, headers=headers)
    data = response.json()

    # Extract color from the response
    user_color = data['data'][0]['color'] if data.get('data') else None

    return user_color

def get_user_id_by_name(username, CLIENT_ID, CLIENT_SECRET):

    token = get_oauth_token(CLIENT_ID, CLIENT_SECRET)

    # Get user ID by username
    url = f'https://api.twitch.tv/helix/users?login={username}'
    headers = {'Client-ID': CLIENT_ID, 'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Extract user ID from the response
    user_id = data['data'][0]['id'] if data.get('data') else None

    return user_id