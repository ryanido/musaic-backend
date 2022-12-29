from django.shortcuts import render
import requests
import json
from django.http import JsonResponse, HttpResponse
from .utils import *


def recently_played(request):
    # Get the code from the request body
    code = request.GET.get('code')
    print(code)
    # Set the headers for the Spotify API request
    headers = {
        'Authorization': 'Bearer {}'.format(code),
    }
    # Make the request to the Spotify API for the user's recently played tracks
    response = requests.get(
        'https://api.spotify.com/v1/me/player/recently-played', headers=headers)
    json_string = json.dumps(response.json())
    # # Write the JSON string to a file
    # with open('example_response_recentl.json', 'w') as f:
    #     f.write(json_string)
    # Check the status code of the response
    if response.status_code == 200:
        # Return the response data as a JSON object
        return JsonResponse(response.json())
    else:
        # Return an error message
        return HttpResponse("Failed to get tracks", status=response.status_code)


def recommendations(request):
    # Get the code from the request body
    code = request.GET.get('code')
    print(code)
    # Set the headers for the Spotify API request
    headers = {
        'Authorization': 'Bearer {}'.format(code),
    }
    # Make the request to the Spotify API for the user's recently played tracks
    artists, genres = artists_genres(code)
    print("%".join(genres))
    songs = tracks(code)
    params = {
        'limit': 10,
        'seed_artists': '%'.join(artists),
        'seed_genres': '%'.join(genres),
        'seed_tracks': '%'.join(songs),
    }
    response = requests.get(
        'https://api.spotify.com/v1/recommendations', headers=headers, params=params)
    print(response.json())
    # Write the JSON string to a file
    # with open('example_response.json', 'w') as f:
    #     f.write(json_string)
    # Check the status code of the response
    if response.status_code == 200:
        # Return the response data as a JSON object
        return JsonResponse(response.json())
    else:
        # Return an error message
        return HttpResponse("Failed to get recommendations", status=response.status_code)
