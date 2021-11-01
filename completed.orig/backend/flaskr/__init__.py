import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  ''' paginates and formats questions
  Method: None
  Parameters: 
  request - HTTP request structure
  selection - variable containing list Question objects
              
  The function gets the page number and uses the QUESTIONS_PER_PAGE
  to organise the questions per page. A slice of questions for the given
  page are then returned

  Return: 
  current_questions - A list of Question objects formatted as 
  a list of dictionaries
  '''
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

  CORS(app, resources={'/': {'origins': '*'}})

  
  #CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response


  @app.route('/categories', methods = ['GET'])
  def retrieve_categories():
    ''' Retrieve categories from the database
    Method: GET
    Endpoint: /categories
    Parameters: 
    None
                
    The function queries the Category model for all categories.
    From the list of Category objects found, a list of dictionaries
    is created and this is returned as a jsonified response together
    with the length of the Category objects list.

    Return: 
    success - True
    categories - list of dictionaries
    total_categories - number of Category objects as an int
    '''
    selection = Category.query.order_by(Category.id).all()
    current_categories = {i.id: i.type for i in selection}

    if len(current_categories) == 0:
      abort(404)

    return jsonify({
      "success" : True,
      "categories" : current_categories,
      "total_categories" : len(Category.query.all())
    })


  @app.route('/questions', methods = ['GET'])
  def retrieve_questions():
    ''' Retrieve questions and categories from the database
    Method: GET
    Endpoint: /questions
    Parameters: 
    None
                
    The function queries the Question model for all questions.
    From the list of Question objects found they are passed to the 
    paginate_questions function to be divided into pages. The function 
    then queries the Category model for all categories.
    From the list of Category objects found, a list of dictionaries
    is created. The success, list of questions, current category,
    a list of all categories and a count of all questions are 
    returned as a jsonified response

    Return: 
    success - True
    questions - list of dictionaries of all the questions
    current_category - None
    categories - list of dictionaries of all categories
    total_questions - a count of all questions as an int
    '''
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


  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    ''' Delete a question
    Method: DELETE
    Endpoint: /questions/<int:question_id>
    Parameters: 
    question_id - the question id as an int
                
    The function queries the Question model for all questions.
    From the list of Question objects found they are passed to the 
    paginate_questions function to be divided into pages. The function 
    then queries the Category model for all categories.
    From the list of Category objects found, a list of dictionaries
    is created. The success, list of questions, current category,
    a list of all categories and a count of all questions are 
    returned as a jsonified response

    Return: 
    success - True
    questions - list of dictionaries of all the questions
    current_category - None
    categories - list of dictionaries of all categories
    total_questions - a count of all questions as an int
    '''
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if (question is None):
        abort(404)

      question.delete()


      return jsonify({
        'success': True,
        'deleted': question_id
      })

    except:
      abort(422)
 

  @app.route('/questions', methods=['POST'])
  def create_question():
    ''' Retrieve questions and categories from the database
    Method: POST
    Endpoint: /questions
    Parameters: 
    From the request body
    question - question as a string
    answer - answer as a string
    difficulty - difficulty rating as an int
    category - category as an int
                
    The function receives a question, answer, difficulty rating and 
    category and instantiates a Question object from this data and 
    inserts the data into the Question model. Then the Question model
    is queried for all questions which are sent to the paginate_questions
    function. The success, created question id, list of current questions
    and count of all questions are sent back as a jsonified response

    Return: 
    success - True
    created - created question id as int
    questions - list of dictionaries of all the questions
    total_questions - a count of all questions as an int
    '''
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
          'total_questions': len(Question.query.all())
        })

    except:
      abort(422)

  
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    ''' Retrieve questions and categories from the database
    Method: POST
    Endpoint: /questions/search
    Parameters: 
    From the request body
    question - question as a string
    answer - answer as a string
    difficulty - difficulty rating as an int
    category - category as an int
                
    The function receives a question, answer, difficulty rating and
    category and instantiates a Question object from this data and
    inserts the data into the Question model. Then the Question
    model is queried for all questions which are sent to the
    paginate_questions function. The success, created question id, 
    list of current questions and countof all questions are sent
    back as a jsonified response

    Return: 
    success - True
    created - created question id as int
    questions - list of dictionaries of all the questions
    total_questions - a count of all questions as an int
    '''
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


  @app.route('/categories/<int:category_id>/questions', methods = ['GET'])
  def get_by_category(category_id):
    ''' Retrieve questions by category id
    Method: GET
    Endpoint: /categories/<int:category_id>
    Parameters: 
    category_id - id of the category as an int
    
                
    The function receives a category id and queries the Category model
    filtering by id to get the category (or a None obj). All questions
    under that category are then extracted from the database and the
    resulting list of Question objects is passed to the 
    paginated_questions function which returns a page of quesions as
    a list of dictionaries. The success, list of current questions, 
    the current category previously passed in as a parameter and a
    count of all the current questions are returned back as a 
    jsonified response.

    Return: 
    success - True
    questions - list of dictionaries of all the questions
    current_category - A string representing the question category type
    total_questions - a count of all questions as an int
    '''
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
  

  @app.route('/quizzes', methods=['POST'])
  def create_quiz():
    ''' Creates a quiz based on a quiz category
    Method: POST
    Endpoint: /quizzes
    Parameters: 
    From the request body
    previous_questions - a list of integers of question ids
    quiz_category - list of dictionarys containing categgory id and type
                
    The function receives a list of previous question ids, and a
    quiz_category list of dictionarys which contains the category id
    and type. If the quiz_category id is '0'; all questions are 
    selected, else only questions which match the quiz_category id
    are selected. These questions are then compared to all previously
    asked questions and only currently unasked questions are listed.
    A random question is taken from the unasked questions list and
    formated into a list of dictionaries. The success, and question
    are sent back as a jsonified response. N.B. when the None obj 
    is sent back this tell the frontend no more questions exist.

    Return: 
    success - True
    question - unasked question as list of dictionaries
    '''
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
        'question': question,
        })         
      
    except:
      abort(422)

  '''Create error handlers for all expected errors'''
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

  return app