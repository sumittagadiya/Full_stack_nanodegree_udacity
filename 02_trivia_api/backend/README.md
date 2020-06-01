# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended.

#### PIP Dependencies

navigate to the `/backend` directory and run:

```bash
pip install -r requirements.txt
```

This will install all of the required packages in the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

#### Frontend Dependencies

This project uses NPM to manage software dependencies. from the `frontend` directory run:

```bash
npm install
```

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## API Reference

### Getting Started

* Backend Base URL: `http://127.0.0.1:5000/`
* Frontend Base URL: `http://127.0.0.1:3000/`
* Authentication: Authentication or API keys are not used in the project yet.

### Error Handling

Errors are returned in the following json format:

```json
      {
        "success": "False",
        "error": 422,
        "message": "Unprocessable entity",
      }
```

The error codes currently returned are:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable
* 500 – internal server error


### Endpoints

#### GET /categories

- General: 
  - Returns all the categories.

- Sample:  `curl http://127.0.0.1:5000/categories`

```json
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "success": true
    }
```

#### GET /questions
- General:
  - Returns all questions
  - questions are in a paginated.
  - pages could be requested by a query string

- Sample: `curl http://127.0.0.1:5000/questions`<br>

```json
        {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 18

}
```

#### DELETE /questions/<int:id\>


- General:
  - Deletes a question by id form the url parameter.

- Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE`

```json
        {
          "success": "True",
          "message": "Question successfully deleted"
        }
```

#### POST /questions

- General:
  - Creates a new question based on a payload.

- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            "question": "Frankie Fredericks represented which African country in athletics?",
            "answer": "Namibia",
            "difficulty": 3,
            "category": "6"
        }'`

```json
{
  "message": "Question successfully created!",
  "success": true
}
```

#### POST /questions/search

- General:
  - returns questions that has the search substring

- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Oscar"}'`

```json
{
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 18
}
```

#### GET /categories/<int:id\>/questions

- General:
  - Gets questions by category using the id from the url parameter.
- Sample: `curl http://127.0.0.1:5000/categories/6/questions`<br>

```json
{
  "current_category": "Sports", 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}

```

#### POST /quizzes

- General
  - Takes the category and previous questions in the request.
  - Return random question not in previous questions.

- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [4, 9],
                                            "quiz_category": {"type": "Art", "id": "2"}}'`

```json
{
  "question": {
    "answer": "Escher", 
    "category": 2, 
    "difficulty": 1, 
    "id": 16, 
    "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
  }, 
  "success": true
}

```

## Authors

- Udacity provided the starter files for the project including the frontend

