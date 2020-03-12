# CommunityRestApi

This python/flask rest api is a community tab prototype for an existing weight loss application. 

###### Project Details
This Rest Api was created with the below tools:
  * Python, Flask, flask_restful, flask_sqlalchemy, flask_httpauth, simplejson
  * Unittest: utilized unittest module
  * Pycharm, sqlite3 database, cURL


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
