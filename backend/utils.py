# Function to format info into desired format
from collections import Counter
import requests
import json
from django.http import JsonResponse, HttpResponse

def top_artist_ids(artists):
    seeds = []
    for item in artists['items']:
        seeds.append(item['id'])
    return seeds[:2]


def top_tracks_ids(tracks):
    seeds = []
    for item in tracks['items']:
        seeds.append(item['id'])
    return seeds[:2]


def get_top_artists_genres(code):
    # Set the headers for the Spotify API request
    headers = {
        'Authorization': 'Bearer {}'.format(code),
    }
    # Make the request to the Spotify API for the user's recently played tracks
    response = requests.get(
        'https://api.spotify.com/v1/me/top/artists', headers=headers)
    json_artists = response.json()
    # Write the JSON string to a file
    # with open('example_response.json', 'w') as f:
    #     f.write(json_string)
    # Check the status code of the response
    if response.status_code == 200:
        artists = top_artist_ids(json_artists)
    
        return artists
    else:
        # Return an error message
        return "error","error"

def get_top_tracks(code):
    # Set the headers for the Spotify API request
    headers = {
        'Authorization': 'Bearer {}'.format(code),
    }
    # Make the request to the Spotify API for the user's recently played tracks
    response = requests.get(
        'https://api.spotify.com/v1/me/top/tracks', headers=headers)
    json_artists = response.json()
    # Write the JSON string to a file
    # with open('example_response.json', 'w') as f:
    #     f.write(json_string)
    # Check the status code of the response
    if response.status_code == 200:
        songs = top_tracks_ids(json_artists)
        print(songs)
        return songs
    else:
        # Return an error message
        return "error"

def get_user_recommendations(code):
    artists = get_top_artists_genres(code)
    songs = get_top_tracks(code)
    response = get_recommendations(code,artists,songs,"hip hop")
    # Check the status code of the response
    if response.status_code == 200:
        # Return the response data as a JSON object
        response = format_recommendations(response.json())
        return JsonResponse(response)
    else:
        # Return an error message
        return HttpResponse("Failed to get recommendations", status=response.status_code)

def get_song_recommendations(code,song,artist):
    response = get_recommendations(code,[artist],[song],"hip hop")
    # Check the status code of the response
    if response.status_code == 200:
        # Return the response data as a JSON object
        response = format_recommendations(response.json())
        return JsonResponse(response)
    else:
        # Return an error message
        return HttpResponse("Failed to get recommendations", status=response.status_code)

def get_recommendations(code,artists,songs,genres):
    headers = {
        'Authorization': 'Bearer {}'.format(code),
    }
    params = {
        'limit': 100,
        'market': 'IE',
        'seed_artists': ",".join(artists),#"4fxd5Ee7UefO4CUXgwJ7IP,3TVXtAsR1Inumwj472S9r4"
        'seed_genres': "hip hop",#' '.join(genres),
        'seed_tracks': ",".join(songs),
    }
    response = requests.get(
        'https://api.spotify.com/v1/recommendations', headers=headers, params=params
        )
    return response

def format_recommendations(response):
    tracks = []
    for track in response['tracks']:
        track_info = {
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'artist_id': track['artists'][0]['id'],
            # 'genre': track['artists'][0]['genres'][0] if track['artists'][0]['genres'] else 'pop',
            'genre':'pop',
            'cover': track['album']['images'][0]['url'],
            'uri':track['uri']
        }
        tracks.append(track_info)
    return {"tracks":tracks}

def format_recently_played(response):
    track_ids = set()
    tracks = []
    for track in response['items']:
        if track['track']['id'] not in track_ids:
            track_info = {
                'id': track['track']['id'],
                'name': track['track']['name'],
                'artist': track['track']['artists'][0]['name'],
                'artist_id': track['track']['artists'][0]['id'],
                # 'genre': track['track']['artists'][0]['genres'][0] if track['track']['artists'][0]['genres'] else None,
                'cover': track['track']['album']['images'][0]['url'],
                'uri': track['track']['uri']
            }
            tracks.append(track_info)
            track_ids.add(track['track']['id'])
    return {"tracks":tracks}


def get_song_recommendationsDB(song):
    return []
