from django.test import TestCase
from .utils import artist_decon
import json
class RecentlyPlayedTestCase(TestCase):
    def test_artist_decon(self):
        # artists = {
        #     'items': [
        #         {'id': 123, 'genres': ['rock', 'pop']},
        #         {'id': 456, 'genres': ['jazz', 'blues']},
        #         {'id': 789, 'genres': ['rap', 'hip hop']},
        #     ]
        # }
        f = open('example_artists.json')
        artists = json.load(f)
        expected_seeds = [123, 456, 789]
        expected_genres = {'rock', 'pop', 'jazz', 'blues', 'rap', 'hip hop'}
        seeds, genres = artist_decon(artists)
        print(seeds)
        print(genres)
        self.assertEqual(seeds, expected_seeds)
        self.assertEqual(genres, expected_genres)

