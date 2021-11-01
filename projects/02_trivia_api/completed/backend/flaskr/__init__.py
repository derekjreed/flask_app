import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  COMPLETED
  '''
  CORS(app, resources={'/': {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  COMPLETED
  '''
  
  #CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  COMPLETED
  '''
  @app.route('/categories', methods = ['GET'])
  def retrieve_categories():
    selection = Category.query.order_by(Category.id).all()
    current_categories = {i.id: i.type for i in selection}
   # current_categories = [i.format() for i in selection]

    if len(current_categories) == 0:
      abort(404)

    return jsonify({
      "success" : True,
      "categories" : current_categories,
      "total_categories" : len(Category.query.all())
    })


  @app.route('/questions', methods = ['GET'])
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    category_select = Category.query.order_by(Category.id).all()
    current_categories = {i.id: i.type for i in category_select}

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      "success" : True,
      "questions" : current_questions,
      "current_category" : None,
      "categories" : current_categories,
      "total_questions" : len(Question.query.all())
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  COMPLETED

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  COMPLETED
  '''
  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if (question is None):
        abort(404)

      question.delete()
      #selection = Question.query.order_by(Question.id).all()
      #current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id
      })

    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  COMPLETED
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)

    #if ((new_question == None) or (new_answer == None) or (new_difficulty == None) or (new_category)):
      #abort(422)

    try:
        question = Question(question=new_question, answer=new_answer,
            difficulty=new_difficulty, category=new_category)
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'created': question.id,
          'questions': current_questions,
          'total_books': len(Question.query.all())
        })

    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  NEEDS TEST  
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', 'None')
    
    try:
      if search_term is not None:
        selection = Question.query.order_by(Question.id)\
               .filter(Question.question.ilike('%{}%'.format(search_term))).all()
        if selection:
           current_questions = paginate_questions(request, selection)
        else:
          current_questions = []

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection)
          })         
      
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question.
  TESTED NPM OK, NEED UNITTEST

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods = ['GET'])
  def get_by_category(category_id):

    category = Category.query.filter(Category.id == category_id).one_or_none()

    if (category is None):
      abort(404)

    try:

      selection = Question.query.filter(Question.category == category_id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        "success" : True,
        "questions" : current_questions,
        "current_category" : category.type,
        "total_questions" : len(Question.query.all())
      })

    except:
        abort(422)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  TESTED NPM OK, NEED UNITTEST
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def create_quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions', 'None')
    quiz_category = body.get('quiz_category', 'None')

    if ((previous_questions is None) or (quiz_category is None)):
      abort(404)

    if (quiz_category['id'] == 0):
      all_questions = Question.query.all()
    else:
      all_questions = Question.query.filter(Question.category == quiz_category['id']).all()

    new_questions = [i for i in all_questions if i.id not in previous_questions]
    

    if new_questions:
      current_question = random.choice(new_questions)
      question = current_question.format()
    else:
      question = None

    
    
    try:

      return jsonify({
        'success': True,
        #'previousQuestions': previous_questions,
        'question': question,
        })         
      
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 204,
      "message": "Bad Request"
      }), 204


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "No Content"
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
        "message": "Method not allowed"
        }), 405      

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable Entity"
        }), 422      
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    