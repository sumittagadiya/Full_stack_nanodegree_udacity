import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from fun import create_mock_question


#psql -h localhost postgres postgres

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '12345', 'localhost:5432', self.database_name)
        self.question = {
            'question': 'Who is best footballer in the world?',
            'answer': 'Leonel Messi',
            'difficulty': 1,
            'category': '6',
        }
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    

    def test_get_all_categories(self):
        """Test for get_all_categories
        Tests for the status code, if success is true,
        if categories is returned and the length of
        the returned categories
        """

        # make request and process response
        response = self.client().get('/categories')
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
    
    def test_get_paginated_questions(self):
        """Test for get all paginated questions
        This tests the return values for a successful
        return of paginated questions
        the assertion that ensures the paginated questions
        is always 10, is determined by a constant that could
        change.
        """
        # make request and process response
        response = self.client().get('/questions')
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)

    def test_404_get_requesting_questions_beyond_valid_page(self):
        """Test for out of bound page
        This test ensures a page that is out of bound
        returns a 404 error
        """

        # make request and process response
        response = self.client().get('/questions?page=10000000')
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_successful_question_delete(self):
    #    """Test for deleting a question.
    #    create_mock_question function is used to prevent having
    #    to drop the database during the running of the test suite.
    #    """

        response = self.client().delete('/questions/5')
        question = Question.query.filter(Question.id == 5).one_or_none()
        data = json.loads(response.data)

        # ensure question does not exist
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Question successfully deleted")
        self.assertEqual(question, None)
        

    def test_delete_question_id_not_exist(self):
        """Tests deletion of question id that doesn't exist
        This tests the error message returned a valid id that
        doesn't exist is used.
        """
        # this tests an id that doesn't exist
        response = self.client().delete('/questions/1211256')
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_question_with_invalid_id(self):
        """Tests deletion of question with invalid id"""
        # this tests an invalid id
        response = self.client().delete('/questions/bjnddskjmv')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_new_questions(self):
        """Test for creating question."""

        # mock data to use as payload for post request
        #post_data = {
        #    'question': 'Who is best footballer in the world?',
        #    'answer': 'Leonel Messi',
        #    'difficulty': 1,
        #    'category': '6',
        #    }
        
        # make request and process response
        response = self.client().post('/questions', json=self.question)
        
        data = json.loads(response.data)
        
        
  
        # assertions to ensure successful request
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question successfully created!')

    def test_new_question_empty(self):
        post_data = {
            'question': '',
            'answer': '',
            'category': 1,
        }
        res = self.client().post('/questions', json=post_data)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Unprocessable entity')

    def test_search_questions(self):
        """Test for searching for a question."""

        request_data = {
            'searchTerm': 'largest lake in Africa',
        }

        # make request and process response
        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_search_term_not_found(self):
        """Test for search term not found."""

        request_data = {
            'searchTerm': 'dfjdtrertwfresyg346474yg',
        }

        # make request and process response
        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions_by_category(self):
        """Test for getting questions by category."""

        # make a request for the Sports category with id of 6
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        #self.assertEqual(data['current_category'], 'Sports')
    
    def test_invalid_category_id(self):
        """Test for invalid category id"""

        # request with invalid category id 1987
        response = self.client().get('/categories/1987/questions')
        data = json.loads(response.data)

        # Assertions to ensure 422 error is returned
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_quiz_All_category_no_previous_question(self):
        res =self.client().post("quizzes",json={"previous_questions": [],
        "quiz_category":  {"type": "click", "id": 0}
        })
        data  = json.loads(res.data)
        self.assertEqual(res.status,'200 OK')
        self.assertEqual(res.status_code,200)
        self.assertTrue(data["question"])

    def test_quiz_by_category_no_previous_question(self):
        res =self.client().post("quizzes",json={"previous_questions": [],
        "quiz_category":  {"type": "click", "id": 6}
        })
        data  = json.loads(res.data)
        self.assertEqual(res.status,'200 OK')
        self.assertEqual(res.status_code,200)
        self.assertTrue(data["question"])

    def test_quiz_by_category_previous_question(self):
        res =self.client().post("quizzes",json={"previous_questions": [14],
        "quiz_category":  {"type": "click", "id": 6}
        })
        data  = json.loads(res.data)
        self.assertEqual(res.status,'200 OK')
        self.assertEqual(res.status_code,200)
        self.assertTrue(data["question"])

   
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
