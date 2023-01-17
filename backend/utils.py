# Function to format info into desired format
from collections import Counter
import requests
import json
from django.http import JsonResponse, HttpResponse

def top_artist_ids(artists):
    seeds = []
    genres = []
    for item in artists['items']:
        seeds.append(item['id'])
        for genre in item['genres']:
            genres.append(genre)
    return seeds[:2], [item for item, _ in Counter(genres).most_common(2)]


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
        artists, genres = top_artist_ids(json_artists)
        print(artists)
        print(genres)
        return artists,genres
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

def get_recommendations(code):
    # Set the headers for the Spotify API request
    headers = {
        'Authorization': 'Bearer {}'.format(code),
    }
    # Make the request to the Spotify API for the user's recently played tracks
    artists, genres = get_top_artists_genres(code)
    songs = get_top_tracks(code)
    params = {
        'limit': 10,
        'market': 'IE',
        'seed_artists': ",".join(artists),#"4fxd5Ee7UefO4CUXgwJ7IP,3TVXtAsR1Inumwj472S9r4"
        'seed_genres': "hip hop",#' '.join(genres),
        'seed_tracks': ",".join(songs),
    }
    response = requests.get(
        'https://api.spotify.com/v1/recommendations', headers=headers, params=params
        )
    print(response.url)
    # Write the JSON string to a file
    # json_string = json.dumps(response.json())
    # with open('example_recommendations.json', 'w') as f:
    #     f.write(json_string)
    # Check the status code of the response
    if response.status_code == 200:
        # Return the response data as a JSON object
        response = format_recommendations(response.json())
        print(response)
        return JsonResponse(response)
    else:
        # Return an error message
        return HttpResponse("Failed to get recommendations", status=response.status_code)

def format_recommendations(response):
    tracks = []
    albums = []
    for track in response['tracks']:
        track_info = {
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'cover': track['album']['images'][0]['url'],
            'uri':track['uri']
        }
        album_info = {
            'id': track['album']['id'],
            'name': track['album']['name'],
            'artist': track['album']['artists'][0]['name'],
            'cover': track['album']['images'][0]['url'],
            'uri': track['album']['uri']
        }
        tracks.append(track_info)
        albums.append(album_info)
    return {"tracks":tracks,"albums": albums}

def format_recently_played(response):
    tracks = []
    for track in response['items']:
        track_info = {
            'id': track['track']['id'],
            'name': track['track']['name'],
            'artist': track['track']['artists'][0]['name'],
            'cover': track['track']['album']['images'][0]['url'],
            'uri': track['track']['uri']
        }
        tracks.append(track_info)
    return tracks



