import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import (Actor, Movie, db_drop_and_create_all, create_dummy_data,
                    setup_db)


''' Environment vars '''

CASTING_ASSISTANT = os.getenv('CASTING_ASSISTANT', 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJiUWVkd1ZMdE5EaVlxWHQwcS1sYyJ9.eyJpc3MiOiJodHRwczovL2Rldi1yYTQxYnV2YS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFhNDAzMTE1NDRmYzMwMDZkNWY2NmI4IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MzgxODQ4MDMsImV4cCI6MTYzODI3MTIwMywiYXpwIjoiV0Z0ZmpJR1ZHMzVUTmRuamxFaXFEb1F3MWs3c1dmRjMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.R1dApQFJqxj44h9Bbiapt9SfWOCPk5SdXqBbh7m1v7p7_Hm9F0URobOhQRtcZQHpCg440oN4UYAyET-Gus4Yap14IkClUMzSmHnf5HkYR-HWDDncsIC4HDdcMP9BeFPZAUIvcGjy_PzUP9Ab_KH6EXjdYwd_d95eXc7rIMhKeoro_PDolj3cxCSWPOIP_hykXCoeuBpdD8nGYzMYD64GWlyYK-oF8STw1IwUBSjgX1a5vALfLOcFN6bhTbBmOaFXhJdT8HAoJWwoAFsr6yFrvcKF9_ykcHPAYqn1EsKXnPuBpP6DmdwaIH7zIpWuR0p7oHYUIMAnQaZxuJ_kjNvPHQ')
CASTING_DIRECTOR = os.getenv('CASTING_DIRECTOR', 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJiUWVkd1ZMdE5EaVlxWHQwcS1sYyJ9.eyJpc3MiOiJodHRwczovL2Rldi1yYTQxYnV2YS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFhNDAzNDFhYzBiOGEwMDY4MGFhYzk3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MzgxODQ5MjEsImV4cCI6MTYzODI3MTMyMSwiYXpwIjoiV0Z0ZmpJR1ZHMzVUTmRuamxFaXFEb1F3MWs3c1dmRjMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.pMccQUVz7KsQotd533lBZtJTpnVFl9LIq1peaKMVarlQfhHZ4MvQpTqWroTUBNwzXRUzRDge2WDJs26ip3pUCFhqQOpwzatfM24yXM_Fm3amixS882d4Jxhzz1eBNdxVTufEhahuQ7ZDy6zTduHd-GT9vP7rnEAqWX38JVSQP-rbBIE7EDgrUajisAOEJ8Pl4AC2YaOnzkEPIvhkVewmqic7zujX2AAJTFAa4jtQ3RsjXSXCRr31xugkUby_2dO0a4PPb05juob3HluNM_s0f8pRYexLGJY1I686uD1eQAlbPVU-S8PREZzBTDKtyD4AS9sHv2S0AzdKN0cukk99YQ')
EXECUTIVE_PRODUCE = os.getenv('EXECUTIVE_PRODUCE', 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJiUWVkd1ZMdE5EaVlxWHQwcS1sYyJ9.eyJpc3MiOiJodHRwczovL2Rldi1yYTQxYnV2YS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFhNDAzNjU2YmQwOGEwMDcwYjYwZmM4IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MzgxODUwOTgsImV4cCI6MTYzODI3MTQ5OCwiYXpwIjoiV0Z0ZmpJR1ZHMzVUTmRuamxFaXFEb1F3MWs3c1dmRjMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.izbAzg0S3vchFKmYOvP1RJXoIyAmQlIIrvMSqmAAt6-ncPNLnSfkM1BACtTrCuKFPfgsItfHiujTAjNGsBunGifT-_a2jwlcYCZ7JVG8f5o4ZT_6h2-J00sW7ZNcIPIGxnvGub6u4Gyr8z7JNXqDXZBvVr3Ks6Zon0WT1_cWVrIdHhF2Slt_T1gMUpBoW81fGWljB58U8Kv0m6lyroS_zsju-kOaQZ_WPj2Opcw3dPF0pxdNCtH9sNkNBvASCbw6gr5BJdUNB_qqlnG4YPle6KMOyMmNCCDMkqfPM0OXeKGuVOtqtY6r4O7jY0wDzSf6ilFID5I_gngGzV8NpV9mtg')


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    @classmethod
    def setUpClass(cls) -> None:
        """Executed before all tests"""
        cls.app = create_app()
        cls.client = cls.app.test_client
        cls.database_name = "agency_test"
        cls.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'password123', 'localhost:5432', cls.database_name)
        setup_db(cls.app, cls.database_path)
        db_drop_and_create_all()
        create_dummy_data()

        # binds the app to the current context
        with cls.app.app_context():
            cls.db = SQLAlchemy()
            cls.db.init_app(cls.app)
            # create all tables

        return super().setUpClass()

    def setUp(self):
        """Executed before each test"""

        """Define test variables and initialize app."""

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

    def tearDown(self):
        """Executed after reach test"""
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        """Executed after all tests"""
        pass
        return super().tearDownClass()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
# Actors

    def test_1_get_paginated_actors_valid_perm(self):
        res = self.client().get('/actors?page=1',
                                headers={"Authorization": CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_2_get_paginated_actors_valid_perm(self):
        res = self.client().get('/actors?page=1',
                                headers={"Authorization": CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_3_get_paginated_actors_noauth(self):
        res = self.client().get('/actors?page=1',
                                headers={"Authorization": None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['code'], 'invalid_header')

    def test_4_get_paginated_actors_page_not_found_valid_perm(self):
        res = self.client().get('/actors?page=100',
                                headers={"Authorization": CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_5_delete_actors_noauth(self):
        res = self.client().delete('/actors/1',
                                   headers={"Authorization": None})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')
        self.assertIsNotNone(actor)

    def test_6_delete_actors_valid_perm(self):
        res = self.client().delete('/actors/1',
                                   headers={"Authorization": EXECUTIVE_PRODUCE})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertIsNone(actor)

    def test_7_delete_actors_beyond_valid_record_invalid_perm(self):
        res = self.client().delete('/actors/20',
                                   headers={"Authorization": CASTING_ASSISTANT})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 20).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertIsNone(actor)

    def test_8_post_actor_correct_data_invalid_perm(self):
        res = self.client().post('/actors', json=self.actor_correct_data,
                                 headers={"Authorization": CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_9_post_actor_correct_data_valid_perm(self):
        res = self.client().post('/actors', json=self.actor_correct_data,
                                 headers={"Authorization": CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['actors']))

    def test_10_post_actor_missing_data_valid_perm(self):
        res = self.client().post('/actors', json=self.actor_partial_data,
                                 headers={"Authorization": EXECUTIVE_PRODUCE})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')

    def test_11_patch_actor_correct_data_invalid_perm(self):
        res = self.client().patch('/actors/2', json=self.actor_partial_data,
                                  headers={"Authorization": CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_12_patch_actor_correct_data_valid_perm(self):
        res = self.client().patch('/actors/2', json=self.actor_partial_data,
                                  headers={"Authorization": CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_13_patch_actor_no_data_valid_perm(self):
        res = self.client().patch('/actors/2', json=self.actor_no_data,
                                  headers={"Authorization": EXECUTIVE_PRODUCE})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')

# Movies

    def test_20_get_paginated_movies_valid_perm(self):
        res = self.client().get('/movies?page=1',
                                headers={"Authorization": CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_21_get_paginated_movies_valid_perm(self):
        res = self.client().get('/movies?page=1',
                                headers={"Authorization": CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_22_get_paginated_movies_noauth(self):
        res = self.client().get('/movies?page=1',
                                headers={"Authorization": None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['code'], 'invalid_header')

    def test_23_get_paginated_movies_page_not_found_valid_perm(self):
        res = self.client().get('/movies?page=100',
                                headers={"Authorization": CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_24_delete_movies_noauth(self):
        res = self.client().delete('/movies/1',
                                   headers={"Authorization": None})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')
        self.assertIsNotNone(movie)

    def test_25_delete_movies_valid_perm(self):
        res = self.client().delete('/movies/1',
                                   headers={"Authorization": EXECUTIVE_PRODUCE})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertIsNone(movie)

    def test_26_delete_movies_beyond_valid_record_invalid_perm(self):
        res = self.client().delete('/movies/20',
                                   headers={"Authorization": CASTING_ASSISTANT})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 20).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertIsNone(movie)

    def test_27_post_movie_correct_data_invalid_perm(self):
        res = self.client().post('/movies', json=self.movie_correct_data,
                                 headers={"Authorization": CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_28_post_movie_correct_data_valid_perm(self):
        res = self.client().post('/movies', json=self.movie_correct_data,
                                 headers={"Authorization": EXECUTIVE_PRODUCE})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['movies']))

    def test_29_post_movie_missing_data_valid_perm(self):
        res = self.client().post('/movies', json=self.movie_partial_data,
                                 headers={"Authorization": EXECUTIVE_PRODUCE})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')

    def test_30_patch_movie_correct_data_invalid_perm(self):
        res = self.client().patch('/movies/2', json=self.movie_partial_data,
                                  headers={"Authorization": CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_31_patch_movie_correct_data_valid_perm(self):
        res = self.client().patch('/movies/2', json=self.movie_partial_data,
                                  headers={"Authorization": EXECUTIVE_PRODUCE})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_32_patch_movie_no_data_valid_perm(self):
        res = self.client().patch('/movies/2', json=self.movie_no_data,
                                  headers={"Authorization": EXECUTIVE_PRODUCE})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
