import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
import sys
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginated_questions(request,questions,QUESTIONS_PER_PAGE):
  page=request.args.get('page',1,type=int)
  start=(page - 1)*QUESTIONS_PER_PAGE
  end=start+QUESTIONS_PER_PAGE
  questions = [question.format() for question in questions]
  current_questions = questions[start:end]
  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''@TODO: Set up CORS. Allow '*' for origins.'''

  CORS(app, resources={'/': {"origins": "*"}})

  '''@TODO: Use the after_request decorator to set Access-Control-Allow'''

  @app.after_request
  def after_request(response):
    """ Set Access Control """
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS')
    return response

  @app.route('/categories')
  def get_all_categories():
    """Get categories endpoint This endpoint returns all categories or
    status code 500 if there is a server error"""
    try:
      categories = Category.query.all()
      #format categories to match front end
      categories_dictionary={}
      for category in categories:
        categories_dictionary[category.id]=category.type

      #return success response
      return jsonify({
        'success':True,
        'categories':categories_dictionary
      }),200
    except Exception:
      abort(500)

  @app.route('/questions')
  def get_questions():
      """Get paginated questions
      This endpoint gets a list of paginated questions based 
      on the page query string parameter and returns a 404
      when the page is out of bound"""

      # get paginated questions and categories
      questions = Question.query.order_by(Question.id).all()
      total_questions = len(questions)
      categories = Category.query.order_by(Category.id).all()

      # Get paginated questions
      current_questions = paginated_questions(request, questions,QUESTIONS_PER_PAGE)
      # return 404 if there are no questions for the page number
      if (len(current_questions) == 0):
        abort(404)

      categories_dictionary = {}
      for category in categories:
        categories_dictionary[category.id] = category.type

      # return values if there are no errors
      return jsonify({
        'success': True,
        'total_questions': total_questions,
        'categories': categories_dictionary,
        'questions': current_questions
      }), 200

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    """Delete specific question
    This endpoint deletes a specific question by the
    id given as a url parameter"""
    try:
      question = Question.query.get(id)
      print("questions",question)
      

      if question is None:
        abort(422)
      else:
        question.delete()
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginated_questions(request, selection,QUESTIONS_PER_PAGE)

      return jsonify({
        'success': True,
        'message': "Question successfully deleted",
        'deleted': id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
        }), 200
    except Exception:
      abort(422)

  @app.route('/questions', methods=['POST'])
  def create_question():
    """This endpoint creates a question.
    A 422 status code is returned if the any of
    the json data is empty."""
    # Get json data from request
    data = request.get_json()
    #data = json.loads(request.data.decode('utf-8'))
    print('Printing Data...............')
    print(data)
    # get individual data from json data
  
    new_question = data.get('question', '')
    new_answer = data.get('answer', '')
    new_difficulty = data.get('difficulty', '')
    new_category = data.get('category', '')
     
    # validate to ensure no data is empty
    if ((new_question == '') or (new_answer == '') or (new_difficulty == '') or (new_category == '')):
      abort(422)
    
    
    print("question ====> ",new_question)
    print("answer ====> ",new_answer)
    print("category ====> ",new_category)
    print("difficulty ====>",new_difficulty)
    
    try:
      # Create a new question instance
      question_record = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
      # save question
      
      question_record.insert()
       
      # return success message
      return jsonify({
        'status_code':200,
        'success': True,
        'message': 'Question successfully created!'
      })
      
    except Exception:
      # return 422 status code if error
      
      print("Error is here")
      print("exception",sys.exc_info())
      abort(422)
      
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    """This endpoint returns questions from a search term. """

    # Get search term from request data
    data = request.get_json()
    search_term = data.get('searchTerm', '')
    # Return 422 status code if empty search term is sent
    if search_term == '':
      abort(422)
    try:
      # get all questions that has the search term substring
      questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

      # if there are no questions for search term return 404
      if len(questions) == 0:
        abort(404)

      # paginate questions
      paginated_question = paginated_questions(request, questions,QUESTIONS_PER_PAGE)
      # return response if successful
      return jsonify({
        'success': True,
        'questions': paginated_question,
        'total_questions': len(Question.query.all())
      }), 200

    except Exception:
      # This error code is returned when 404 abort
      # raises exception from try block
      abort(404)

  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    """This endpoint handles getting questions by category"""

    # get the category by id
    category = Category.query.filter_by(id=id).one_or_none()

    # abort 400 for bad request if category isn't found
    if (category is None):
      abort(422)

    questions = Question.query.filter_by(category=id).all()
    # paginate questions
    paginated_question = paginated_questions(request, questions,QUESTIONS_PER_PAGE)

    # return the results
    return jsonify({
      'success': True,
      'questions': paginated_question,
      'total_questions': len(questions),
      'current_category': category.type
    })

  @app.route("/quizzes",methods=["POST"])
  def get_quiz_questions():
    try:
      body = request.get_json()
      previous_question = body.get('previous_questions')
      quiz_category = int(body.get('quiz_category')['id'])
      category = Category.query.get(quiz_category)
      # if category is not None 
      if not category == None:
        # check if there are some previous questions so that we will not show those question
        # again
        if  "previous_questions"  in body and len(previous_question) > 0 :
          # filtered out category and filterd out previous question
          questions = Question.query.filter(Question.id.notin_(
            previous_question), Question.category == category.id).all()
          
        # if there are no previous question then check for category and if category is all
        # then show all question
        else:
          print("in first else",category)
          questions = Question.query.filter_by(category = category.id).all()
      else:
        # if category is none then only check for previous question filter
        if "previous_questions" in body and len(previous_question) > 0:
          questions = Question.query.filter(Question.id.notin_(previous_question)).all()
        # if previous question is None and category is also None then show all
        else:
          questions = Question.query.all()
      max = len(questions) - 1
      if max > 0:
          questions = questions[random.randint(0, max)].format()

      else:
          questions = False
      print(questions)
      return jsonify({
          'status': 200,
          "success": True,
          "question": questions
      })          
    except:
      print(sys.exc_info())
      abort(500)

  # Error handler for Bad request error (400)

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request error'
    }), 400

  # Error handler for resource not found (404)
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }), 404

  # Error handler for internal server error (500)
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'An error has occured, please try again'
    }), 500

  # Error handler for unprocesable entity (422)
  @app.errorhandler(422)
  def unprocesable_entity(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable entity'
    }), 422

  return app



