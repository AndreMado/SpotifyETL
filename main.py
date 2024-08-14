from dotenv import load_dotenv
import os
import base64
from requests import post,get
from icecream import ic
import pandas as pd
from datetime import datetime
import sqlite3
import sqlalchemy
from sqlalchemy.orm import sessionmaker


##############################################################EXTRACT BLOCK OF CODE####################################################################################

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET_KEY")
DATABASE_LOCATION = "sqlite:///artist_top_tracks.sqlite"

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
    console_log("The data has been turned into a Data Frame, ready for a validation check .....")
    return df

##############################################################TRANSFORM OR VALIDATION BLOCK OF CODE######################################################################

def valid_data_check(df: pd.DataFrame) -> bool:
    #Check if the Data Frame is empty
    if df.empty:
        console_log("No data here, finishing execution")
        return False
    
    #Primary Key Check
    if pd.Series(df['song_name']).is_unique:
        pass
    else:
        raise Exception("Primary Key Check is violated, something wrong with the dataframe")
    
    #Check for null values
    if df.isnull().values.any():
        raise Exception("Null values has beem detected into the Data Frame.")
    
    return True


##########################################################################LOAD BLOCK OF CODE##############################################################################

def load_db(df: pd.DataFrame) -> bool:
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('artist_top_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS top_tracks_badbunny(
        song_name VARCHAR(200) PRIMARY KEY,
        song_release_date VARCHAR(200),
        realese_date_precision VARCHAR(200),
        popularity_rank VARCHAR(200),
        duration_in_ms VARCHAR(200),
        adult_letter VARCHAR(200)
    )
    """

    cursor.execute(sql_query)
    try:
        df.to_sql("top_tracks_badbunny",engine, index=False, if_exists='append')
        console_log("The data has been insert in the database")
    except:
        ic("Data already exist in the database")

    conn.close()
    console_log("CLosing the database conection sucessfully")
    return True


    






if __name__ == "__main__":
    console_log("Initializating ETL process, extraction begins, getting token from Spotify...")
    token = get_token()
    #ic(search_album("Swimming", token))
    artist_input = input("Insert artist name: ")
    artist_id = search_artist(artist_input, token)
    data = artist_top_tracks(artist_id, token)
    df = to_dataframe(data)

    if valid_data_check(df):
        console_log("Validation complete, proceed to Load stage")

    ic(load_db(df))
    



    

    #for i, song in enumerate(data):
    #    ic(f"{i + 1}. {song["name"]}")
    
    
    #Testing working remote
    #Testing git 
