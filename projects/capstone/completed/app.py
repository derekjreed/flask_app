import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from models import Actor, Movie, setup_db


ITEMS_PER_PAGE = 2


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

    @app.route('/actors', methods=['GET'])
    def get_actors():
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
        #current_actors = {i.id: i.type for i in selection}

        if len(current_actors) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "actors": current_actors,
            "total_actors": len(Actor.query.all())
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    def get_actor(actor_id):
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
    def delete_question(actor_id):
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
            })

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

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
