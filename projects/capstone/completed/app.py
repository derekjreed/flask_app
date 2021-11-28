import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
#from flask_sqlalchemy import SQLAlchemy

from auth import AuthError, requires_auth
from models import Actor, Movie, setup_db

ITEMS_PER_PAGE = 5


def paginate_items(request, selection):
    ''' paginates and formats items
    Method: None
    Parameters:
    request - HTTP request structure
    selection - variable containing list objects
    The function gets the page number and uses the ITEMS_PER_PAGE
    to organise the items per page. A slice of items for the given
    page are then returned
    Return:
    current_items - A list of objects formatted as
    a list of dictionaries
    '''
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={'/': {'origins': '*'}})
    # CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTION')
        return response

#
# Actor APIs
#

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        ''' Get actors from the database
        Method: GET
        Endpoint: /actors
        Parameters:
        None
        The function queries the Actor model for all actors.
        From the list of Actor objects found, a list of dictionaries
        is created and this is returned as a jsonified response together
        with the length of the Actor objects list.
        Return:
        success - True
        actors - list of dictionaries
        total_actors - number of Actor objects as an int
        '''
        selection = Actor.query.order_by(Actor.id).all()
        current_actors = paginate_items(request, selection)
        # current_actors = {i.id: i.type for i in selection}

        if len(current_actors) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "actors": current_actors,
            "total_actors": len(Actor.query.all())
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):
        ''' Retrieve actor by id
        Method: GET
        Endpoint: /actors/<int:actor_id
        Parameters:
        actor_id - id of the actor as an int
        The function receives a actor id and queries the Actor model
        filtering by id to get the actor (or a None obj). All questions
        under that actor are then extracted from the database and the
        resulting list of Question objects is passed to the
        paginated_questions function which returns a page of quesions as
        a list of dictionaries. The success, list of current questions,
        the current actor previously passed in as a parameter and a
        count of all the current questions are returned back as a
        jsonified response.
        Return:
        success - True
        questions - list of dictionaries of all the questions
        current_actor - A string representing the question actor type
        total_questions - a count of all questions as an int
        '''
        actor = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        if (actor is None):
            abort(404)

        try:

            return jsonify({
                "success": True,
                "actor": actor.format(),
            }), 200

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        ''' Delete a actor
        Method: DELETE
        Endpoint: /actors/<int:actor_id>
        Parameters:
        actor_id - the actor id as an int
        The function queries the Actor model for actor_id.
        If the actor id exists the actor entry is deleted.
        The success and deleted actor id are
        returned as a jsonified response.
        Return:
        success - True
        deleted - actor_id
        '''
        try:
            actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()

            if (actor is None):
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor_id
            }), 200

        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        ''' Add a new question to the database
        Method: POST
        Endpoint: /actors
        Parameters:
        From the request body
        question - question as a string
        answer - answer as a string
        difficulty - difficulty rating as an int
        category - category as an int
        The function receives a question, answer, difficulty rating and
        category and instantiates a Question object from this data and
        inserts the data into the Question model. Then the Question model
        is queried for all actors which are sent to the paginate_actors
        function. The success, created question id, list of current actors
        and count of all actors are sent back as a jsonified response
        Return:
        success - True
        created - created question id as int
        actors - list of dictionaries of all the actors
        total_actors - a count of all actors as an int
        '''
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            actor = Actor(name=new_name, age=new_age,
                          gender=new_gender)
            actor.insert()

            selection = Actor.query.order_by(Actor.id).all()
            current_actors = paginate_items(request, selection)

            return jsonify({
                'success': True,
                'created': actor.id,
                'actors': current_actors,
                'total_actors': len(Actor.query.all())
            }), 200

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(payload, actor_id):
        ''' Patch for a question
        Method: POST
        Endpoint: /actors/<int:actor_id>
        Parameters:
        From the request body
        actor - question as a string
        age - answer as a string
        gender - difficulty rating as an int
        The function receives a search string from the request body.
        The string is searched for in the Question model (case
        insensitive search). Each question which matches is placed in
        a list which is paginated else an empty list is created.
        The success, list of current actors matched and count of
        all actors are sent back as a jsonified response
        Return:
        success - True
        actors - list of dictionaries of all the actors
        total_actors - a count of all actors as an int
        '''
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if new_name is None and new_age is None and new_gender is None:
            abort(422)

        try:

            actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()

            if new_name is not None:
                actor.name = new_name
            if new_age is not None:
                actor.age = new_age
            if new_gender is not None:
                actor.gender = new_gender

            actor.update()

            selection = Actor.query.order_by(Actor.id).all()
            current_actors = paginate_items(request, selection)

            return jsonify({
                'success': True,
                'actors': current_actors,
                'total_actors': len(Actor.query.all())
            }), 200

        except:
            abort(422)


#
# Movie APIs
#

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        ''' Get movies from the database
        Method: GET
        Endpoint: /movies
        Parameters:
        None
        The function queries the Movie model for all movies.
        From the list of Movie objects found, a list of dictionaries
        is created and this is returned as a jsonified response together
        with the length of the Movie objects list.
        Return:
        success - True
        movie - list of dictionaries
        total_movie - number of Movie objects as an int
        '''
        selection = Movie.query.order_by(Movie.id).all()
        current_movies = paginate_items(request, selection)
        # current_movies = {i.id: i.type for i in selection}

        if len(current_movies) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "movies": current_movies,
            "total_movies": len(Movie.query.all())
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):
        ''' Retrieve movie by id
        Method: GET
        Endpoint: /movies/<int:movie_id
        Parameters:
        movie_id - id of the movie as an int
        The function receives a movie id and queries the Movie model
        filtering by id to get the actor (or a None obj). All questions
        under that actor are then extracted from the database and the
        resulting list of Question objects is passed to the
        paginated_questions function which returns a page of quesions as
        a list of dictionaries. The success, list of current questions,
        the current actor previously passed in as a parameter and a
        count of all the current questions are returned back as a
        jsonified response.
        Return:
        success - True
        movie - 
        current_actor - A string representing the question actor type
        total_questions - a count of all questions as an int
        '''
        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()

        if (movie is None):
            abort(404)

        try:

            return jsonify({
                "success": True,
                "movie": movie.format(),
            }), 200

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        ''' Delete a movie
        Method: DELETE
        Endpoint: /movies/<int:movie_id>
        Parameters:
        movie_id - the movie id as an int
        The function queries the Movie model for movie_id.
        If the movie id exists the movie entry is deleted.
        The success and deleted movie id are
        returned as a jsonified response.
        Return:
        success - True
        deleted - movie_id
        '''
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if (movie is None):
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id
            }), 200

        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        ''' Add a new question to the database
        Method: POST
        Endpoint: /movies
        Parameters:
        From the request body
        question - question as a string
        answer - answer as a string
        difficulty - difficulty rating as an int
        category - category as an int
        The function receives a question, answer, difficulty rating and
        category and instantiates a Question object from this data and
        inserts the data into the Question model. Then the Question model
        is queried for all movies which are sent to the paginate_movies
        function. The success, created question id, list of current movies
        and count of all movies are sent back as a jsonified response
        Return:
        success - True
        created - created question id as int
        movies - list of dictionaries of all the movies
        total_movies - a count of all movies as an int
        '''
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            selection = Movie.query.order_by(Movie.id).all()
            current_movies = paginate_items(request, selection)

            return jsonify({
                'success': True,
                'created': movie.id,
                'movies': current_movies,
                'total_questions': len(Movie.query.all())
            }), 200

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(payload, movie_id):
        ''' Patch for a question
        Method: POST
        Endpoint: /movies/<int:movie_id>
        Parameters:
        From the request body
        movie - question as a string
        age - answer as a string
        gender - difficulty rating as an int
        The function receives a search string from the request body.
        The string is searched for in the Question model (case
        insensitive search). Each question which matches is placed in
        a list which is paginated else an empty list is created.
        The success, list of current movies matched and count of
        all movies are sent back as a jsonified response
        Return:
        success - True
        movies - list of dictionaries of all the movies
        total_movies - a count of all movies as an int
        '''
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if new_title is None and new_release_date is None:
            abort(422)

        try:

            movie = Movie.query.filter(
                Movie.id == movie_id).one_or_none()

            if new_title is not None:
                movie.title = new_title
            if new_release_date is not None:
                movie.release_date = new_release_date

            movie.update()

            selection = Movie.query.order_by(Movie.id).all()
            current_movies = paginate_items(request, selection)

            return jsonify({
                'success': True,
                'movies': current_movies,
                'total_questions': len(Movie.query.all())
            }), 200

        except:
            abort(422)

    '''Create error handlers for all expected errors'''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(AuthError)
    def unauthorized(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
