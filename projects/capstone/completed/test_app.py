import json
import os
import unittest
import time

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import (Actor, Movie, db_create_all,
                    setup_db)


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'password123', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db_create_all()

        self.actor_correct_data = {
            'name': 'James Don Senior',
            'age': 58,
            'gender': 'Male',
        }

        self.actor_partial_data = {
            'name': 'James Don Junior',
            'age': 28,
        }

        self.actor_no_data = {
        }

        self.movie_correct_data = {
            'title': 'The long time',
            'release_date': '2022-01-01'
        }

        self.movie_partial_data = {
            'title': 'The best ever'
        }

        self.movie_no_data = {
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
# Actors

    def test_1_get_paginated_actors(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_2_get_paginated_actors_page_not_found(self):
        res = self.client().get('/actors?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_8_delete_actors(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)

    def test_4_delete_actors_beyond_valid_record(self):
        res = self.client().delete('/actors/20')
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 20).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertEqual(actor, None)

    def test_5_post_actor_correct_data(self):
        res = self.client().post('/actors', json=self.actor_correct_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['actors']))

    def test_6_post_actor_missing_data(self):
        res = self.client().post('/actors', json=self.actor_partial_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')

    def test_7_patch_actor_correct_data(self):
        res = self.client().patch('/actors/1', json=self.actor_partial_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_3_patch_actor_no_data(self):
        res = self.client().patch('/actors/1', json=self.actor_no_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')

# Movies

    def test_9_get_paginated_movies(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_10_get_paginated_movies_page_not_found(self):
        res = self.client().get('/movies?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_15_delete_movies(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(movie, None)

    def test_12_delete_movies_beyond_valid_record(self):
        res = self.client().delete('/movies/20')
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 20).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertEqual(movie, None)

    def test_13_post_movie_correct_data(self):
        res = self.client().post('/movies', json=self.movie_correct_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['movies']))

    def test_14_post_movie_missing_data(self):
        res = self.client().post('/movies', json=self.movie_partial_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')

    def test_11_patch_movie_correct_data(self):
        res = self.client().patch('/movies/1', json=self.movie_partial_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_16_patch_movie_no_data(self):
        res = self.client().patch('/movies/1', json=self.movie_no_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
