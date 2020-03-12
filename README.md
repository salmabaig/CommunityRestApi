# CommunityRestApi

This python/flask rest api is a community tab prototype for an existing weight loss application. 

###### Project Details
This Rest Api was created with the below tools:
  * Python, Flask, flask_restful, flask_sqlalchemy, flask_httpauth, simplejson
  * Unittest: utilized unittest module
  * Pycharm, sqlite3 database, cURL

Files included: 
 - restApi.py - holds rest api code for community table
 - Test_api.py - unittest file for rest api
 - db.sqlite - sample DB from manual test run
 - test.db - sample DB from unittest run


## Design Details: 
The following highlights the notes from design phase:


 * User table : In order to keep track of who is posting question/answer and marking favorite question/answer, user table is required. Certain actions require user authentication. Utilizing sqlite3 database for temporary storage.  
    * Rows for User Table: u_id, username, password
 * Requirement 1: Post questions for other users  
    * Questions table is required.
    * Table rows: q_id, question, userId(to keep track of author of question.)
 * Requirement 2: Answer question posted by others
    * Answer table is required
    * Table rows: a_id, answer, user_Id, q_id(link question and answer)
 * Requirement 3: View questions
    * Requires a retrieval query from question table
 * Requirement 4: View responses to questions
    * Requires retrieval from both question and answer table.
 * Requirement 5: bookmark question or answers
    * Requires table to mark favorite question and answer
       * Fave_q table is required
         * Rows: user_id, q_id
       * Fave_a table is required
         * Rows: user_id, a_id
      * Queries fav_q and fav_a table to display to user. 
      
      
## Testing Instructions

###### Testing with unittest file: 
* Place restApi.py and test_api.py in same file
* Run the following command
    - python -m unittest test_api.py
* Database file, test.db, will be produced

###### Manual testing without unittest test file: 

* Written with Python 3.6.4
* Please be sure following packages are installed with pip(flask, flask_restful, flask_sqlalchemy, flask_httpauth, passlib
* Go to directory with restApi.py and run following command
 - python restApi.py
* Use cURL to test functionality: 
 - Add new user: curl -i -X POST -H "Content-Type: application/json" -d '{"username":"salma","password":"siddiqua"}' http://127.0.0.1:5000/api/users
 - Add new question : curl -u salma:siddiqua -i -X POST -H "Content-Type: application/json" -d '{"question":"How do you loose weight?"}' http://127.0.0.1:5000/api/questions
 - Add answer: curl -u salma:siddiqua -i -X POST -H "Content-Type: application/json" -d '{"answer":"Yes", "q_id":"3"}' http://127.0.0.1:5000/api/answers
 - Add favorite question: curl -u salma:siddiqua -i -X POST -H "Content-Type: application/json" -d '{"q_id”:”1”}’ http://127.0.0.1:5000/api/favQ
 - Add favorite answer: curl -u salma:siddiqua -i -X POST -H "Content-Type: application/json" -d '{"a_id”:”1”}’ http://127.0.0.1:5000/api/favA
 - View favorite questions: curl -u salma:siddiqua -i -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/api/view/favQ
 - View favorite answers: curl -u salma:siddiqua -i -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/api/view/favA
 - View all questions: curl -u salma:siddiqua -i -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/api/view/allQ
 - View all questions and responses: curl -u salma:siddiqua -i -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/api/view/allQA

* Database file, db.sqlite, will be created



