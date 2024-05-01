import base64
from requests import post, get
import json
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

from django.conf import settings

                               # use up.get_url_type(url) to get playlist/song/album type (returns str) 

client_id = settings.SOCIAL_AUTH_SPOTIFY_ID
client_secret = settings.SOCIAL_AUTH_SPOTIFY_SECRET
# client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_token():
    """ Get Spotify token to access artist and track info """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_popularity(content_type = "track", content_name = "", input_id = ""):
    if content_name == "" and input_id == "":
        return None
    
    token = get_token()
    if content_name != "" and input_id == "":
        result = user_search(token, content_name, search_type=content_type)
        if result is None:
            return None
        id = result["id"]
    else:
        id = input_id

    """ Search for content and return items associated with content"""
    url = f"https://api.spotify.com/v1/{content_type}s"
    headers = get_auth_header(token)
    query = f"/{id}"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    """ Get content popularity """
    if content_type == "playlist":
        popularity = get_avg_popularity(result, json_result)
    else:
        popularity = json_result['popularity']

    """ Get name of content """
    name = json_result["name"]
    if content_type != "playlist":
        name = name + ' - ' + json_result["artists"][0]["name"]

    """ Get image of the content"""
    if content_type == "track":
        image = json_result["album"]["images"][0]["url"]
    else:
        image = json_result["images"][0]["url"]

    return popularity, name, image
    

def get_avg_popularity(result, json_result):
    sum = 0
    num_tracks = 0

    for track in json_result["tracks"]["items"]:
        result = track["track"]
        sum += result["popularity"]
        num_tracks += 1
    
    return sum // num_tracks


def user_search(token, track_name, search_type = "track"):
    """ Search for a track and return items associated with track """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type={search_type}&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)[f"{search_type}s"]["items"]
    
    if len(json_result) == 0:
        print(f"No {search_type} with this name exists...")
        return None
    
    return json_result[0]
