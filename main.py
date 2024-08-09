from dotenv import load_dotenv
import os
import base64
from requests import post,get
from icecream import ic

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("SECRET_KEY")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type" :"application/x-www-form-urlencoded",

    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers= headers, data= data).json()
    token = result["access_token"]

    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_album(album, token):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={album}&type=album&track&limit=1"

    query_url = url + query
    result = get(query_url, headers= headers).json()
    return result

def search_artist(artist_name, token):
    url = "https://api.spotify.com/v1/search"
    header = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers= header).json()
    result = result["artists"]["items"]
    if len(result) == 0:
        print("The artists don't exist anymore....")
    else:
        return result[0]["id"]

def  artist_top_tracks(artist_id, token):
    url = "https://api.spotify.com/v1/artists/"
    header = get_auth_header(token)
    query = f"{artist_id}/top-tracks"
    url_query = url + query
    result = get(url_query, headers= header).json()["tracks"]
    return result

if __name__ == "__main__":
    token = get_token()
    #ic(search_album("Swimming", token))
    artist_id = search_artist("Bad Bunny", token)
    ic(artist_top_tracks(artist_id, token))