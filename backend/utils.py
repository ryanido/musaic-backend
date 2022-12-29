# Function to format info into desired format
from collections import Counter
import requests

def artist_decon(artists):
    seeds = []
    genres = []
    for item in artists['items']:
        seeds.append(item['id'])
        for genre in item['genres']:
            genres.append(genre)
    return seeds[:2], [item for item, _ in Counter(genres).most_common(2)]


def tracks_decon(tracks):
    seeds = []
    for item in tracks['items']:
        seeds.append(item['id'])
    return seeds[:2]


def artists_genres(code):
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
        artists, genres = artist_decon(json_artists)
        print(artists)
        print(genres)
        return artists,genres
    else:
        # Return an error message
        return "error","error"

def tracks(code):
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
        songs = tracks_decon(json_artists)
        print(songs)
        return songs
    else:
        # Return an error message
        return "error"