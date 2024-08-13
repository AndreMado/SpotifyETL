from dotenv import load_dotenv
import os
import base64
from requests import post,get
from icecream import ic
import pandas as pd
from datetime import datetime

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET_KEY")

def console_log(message):
    timestamp_format = '%Y-%h-%d:%H-%M-%S'
    now = datetime.now()
    timestamp= now.strftime(timestamp_format)
    with open("log.txt", "a") as log:
        log.write(timestamp + ' : ' + message + '\n')

def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
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
    console_log("The token has been gotten, time to create de Authorization header")

    return token

def get_auth_header(token):
    console_log("Header ready, calling search artist function...")
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
        console_log("Spotify give us an 200 OK code, sucess in search")
        return result[0]["id"]
        

def  artist_top_tracks(artist_id, token):
    url = "https://api.spotify.com/v1/artists/"
    header = get_auth_header(token)
    query = f"{artist_id}/top-tracks"
    url_query = url + query
    result = get(url_query, headers= header).json()["tracks"]
    console_log("Connecting with the top 10 tracks of the artist")
    return result

if __name__ == "__main__":
    token = get_token()
    #ic(search_album("Swimming", token))
    #artist_input = input("Insert artist name: ")
    artist_id = search_artist("Ariana Grande", token)
    data = artist_top_tracks(artist_id, token)
    
    def to_dataframe(data):
        songs_name= []
        songs_release_date = []
        release_date_precision = []
        popularity = []
        duration_ms = []
        explicit = []


        for song in data:
            songs_name.append(song["name"])
            songs_release_date.append(song["album"]["release_date"])
            release_date_precision.append(song["album"]["release_date_precision"])
            popularity.append(song["popularity"])
            duration_ms.append(song["duration_ms"])
            explicit.append(song["explicit"])


        songs_dict={
            "song_name":songs_name,
            "song_release_date":songs_release_date,
            "realese_date_precision": release_date_precision,
            "popularity_rank":popularity,
            "duration_in_ms": duration_ms,
            "adult_letter": explicit
        }

        df = pd.DataFrame(data=songs_dict)
        return df

    ic(df)
    console_log("Initializating ETL process, extraction begins, getting token from Spotify...")

    #for i, song in enumerate(data):
    #    ic(f"{i + 1}. {song["name"]}")
    
    
    #Testing working remote
    #Testing git 
