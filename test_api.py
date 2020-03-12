#!/usr/bin/env python
import unittest,json, os, base64
from restApi import app, db

TEST_DB = 'test.db'

class TestApi(unittest.TestCase):
    # Basic setup for app and test database
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(TEST_DB)
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        self.app = app.test_client() #???
        db.drop_all()
        db.create_all()

    def test_api(self):
        username1,username2,username3 = "Salma","First","Jet"

        loginInfo1 = json.dumps({ "username" : username1, "password" : "siddiqua"})
        loginInfo2 = json.dumps({"username": username2,"password": "last"})
        loginInfo3 = json.dumps({"username": username3,"password": "cakes"})

        print("Adding Users. \n")
        #Adding in three new User
        response = self.app.post('/api/users', headers={"Content-Type": "application/json"}, data=loginInfo1)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(username1,data['username'])
        self.assertEqual(200, response.status_code)
        print("New User Added: ")
        print(data)

        response = self.app.post('/api/users', headers={"Content-Type": "application/json"}, data=loginInfo2)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(username2, data['username'])
        self.assertEqual(200, response.status_code)
        print("New User Added: ")
        print(data)

        response = self.app.post('/api/users', headers={"Content-Type": "application/json"}, data=loginInfo3)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(username3, data['username'])
        self.assertEqual(200, response.status_code)
        print("New User Added: ")
        print(data)
        print("\n")

        # Adding in existing user
        response = self.app.post('/api/users', headers={"Content-Type": "application/json"}, data=loginInfo3)
        print("Result for adding in an existing user:")
        print(response)
        self.assertEqual(400, response.status_code)

        # Adding in null user
        response = self.app.post('/api/users', headers={"Content-Type": "application/json"})
        print("Result for adding in an null user:")
        print(response)
        self.assertEqual(400, response.status_code)
        print("********************************************************\n")

        # Adding questions---------------------------------------------------------------------------
        print("Adding in questions/posting questions\n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username2 + ":" + "last", 'ascii')).decode('ascii')}

        question1 = "How do you loose weight?"
        QInfo1 = json.dumps({ "question": question1})

        response = self.app.post('/api/questions', headers=headers, data=QInfo1)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(question1, data['question'])
        self.assertEqual(200, response.status_code)
        print("Adding Question:")
        print(data)
        print(response)
        print("\n")

        headers = {
            'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username1 + ":" + "siddiqua", 'ascii')).decode('ascii')}

        question2 = "What is the keto diet?"
        QInfo2 = json.dumps({"question": question2})

        response = self.app.post('/api/questions', headers=headers, data=QInfo2)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(question2, data['question'])
        self.assertEqual(200, response.status_code)
        print("Adding in Question:")
        print(data)
        print(response)
        print("\n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username3 + ":" + "cakes", 'ascii')).decode('ascii')}

        question3 = "How much water should you drink everyday?"
        QInfo3 = json.dumps({"question": question3})

        response = self.app.post('/api/questions', headers=headers, data=QInfo3)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(question3, data['question'])
        self.assertEqual(200, response.status_code)
        print("Addding in Question:")
        print(data)
        print(response)
        print("\n")

        # Making a request without any question parameter
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username3 + ":" + "cakes", 'ascii')).decode('ascii')
        }
        response = self.app.post('/api/questions', headers=headers)
        data = json.loads(response.get_data(as_text=True))
        if(self.assertEqual(400, response.status_code)):
            self.assertEqual(question3, data['question'])
        print("Attempting to make request without question parameter")
        print(response)
        print("\n")

        #Making a request to add question with invalid user/password
        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes("Test" + ":" + "cakes", 'ascii')).decode('ascii')}

        question3 = "How much water should you drink everyday?"
        QInfo3 = json.dumps({"question": question3})

        response = self.app.post('/api/questions', headers=headers, data=QInfo3)
        self.assertEqual(401, response.status_code)
        print("Attempting to add question without authentication")
        print(response)
        print("****************************************\n")

        #Add Answer-----------------------------------------------------------------------------------------

        print("Adding in answers/responding to questions\n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username3 + ":" + "cakes", 'ascii')).decode('ascii')}

        AInfo1 = json.dumps({"answer":"Diet and Exercise", "q_id": "1"})

        response = self.app.post('/api/answers', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("Adding in Answer:")
        print(data)
        print(response)
        self.assertEqual("Diet and Exercise", data['answer'])
        self.assertEqual(200, response.status_code)
        print("\n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username1 + ":" + "siddiqua", 'ascii')).decode('ascii')}

        AInfo1 = json.dumps({ "answer": "Eat only protein and vegetables.", "q_id": "2"})

        response = self.app.post('/api/answers', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("Adding in Answer:")
        print(data)
        print(response)
        self.assertEqual("Eat only protein and vegetables.", data['answer'])
        self.assertEqual(200, response.status_code)
        print("\n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username2 + ":" + "last", 'ascii')).decode('ascii')}

        AInfo1 = json.dumps({"answer": "One gallon everyday.","q_id": "3"})

        response = self.app.post('/api/answers', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("Adding in Answer:")
        print(data)
        print(response)
        self.assertEqual("One gallon everyday.", data['answer'])
        self.assertEqual(200, response.status_code)
        print("\n")

        #Testing invalid user/password
        AInfo1 = json.dumps({ "answer": "One liter everyday.","q_id": "3"})

        response = self.app.post('/api/answers', headers={"Content-Type": "application/json"}, data=AInfo1)
        print("Attempting to add answer with authentication")
        print(response)
        self.assertEqual(401, response.status_code)
        print("*********************************\n")

    #Add Favorite Question---------------------------------------------

        print("Marking Favorite Questions.\n")
        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username1 + ":" + "siddiqua", 'ascii')).decode('ascii')}

        AInfo1 = json.dumps({"q_id": "1"})

        response = self.app.post('/api/favQ', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("Adding in favorite Question for User Salma")
        print(data)
        print(response)
        self.assertEqual(1, data['question'])
        self.assertEqual(200, response.status_code)
        print("\n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username1 + ":" + "siddiqua", 'ascii')).decode('ascii')}

        AInfo1 = json.dumps({"q_id": "2"})

        response = self.app.post('/api/favQ', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("Adding in favorite Question for User Salma")
        print(data)
        print(response)
        self.assertEqual(2, data['question'])
        self.assertEqual(200, response.status_code)
        print('\n')

        # Adding the same question as a favorite, returns error
        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username1 + ":" + "siddiqua", 'ascii')).decode('ascii')}

        AInfo1 = json.dumps({"q_id": "2"})

        response = self.app.post('/api/favQ', headers=headers, data=AInfo1)
        print("Attempting to favorite a question already added")
        print(response)
        self.assertEqual(400, response.status_code)
        print('\n')

        print("************************************************************\n")

        # Adding Favortie answers-----------------------------------------------------------
        print("Marking Favorite Answers.\n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username1 + ":" + "siddiqua", 'ascii')).decode('ascii')}

        AInfo1 = json.dumps({"a_id": "1"})
        response = self.app.post('/api/favA', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("Adding in favorite answer for User Salma")
        print(data)
        print(response)
        self.assertEqual(1, data['answer'])
        self.assertEqual(200, response.status_code)
        print('\n')

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username2 + ":" + "last", 'ascii')).decode('ascii')}

        AInfo1 = json.dumps({"a_id": "1"})

        response = self.app.post('/api/favA', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("Adding in favorite answer for User Salma")
        print(data)
        print(response)
        self.assertEqual(1, data['answer'])
        self.assertEqual(200, response.status_code)
        print("\n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username2 + ":" + "last", 'ascii')).decode('ascii')}

        AInfo1 = json.dumps({"a_id": "1"})

        response = self.app.post('/api/favA', headers=headers, data=AInfo1)
        print("Attempting to favorite an answer already added")
        print(response)
        self.assertEqual(400, response.status_code)
        print("*********************************************\n")

        # View All Questions Favorited: ---------------------------------------------------
        print("View all favorite questions. \n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username1 + ":" + "siddiqua", 'ascii')).decode('ascii')}

        response = self.app.post('/api/view/favQ', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("Viewing all Favorite Questions by User Salma")
        print(data)
        print(response)
        self.assertEqual(200, response.status_code)
        print("\n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username3 + ":" + "cakes", 'ascii')).decode('ascii')}

        response = self.app.post('/api/view/favQ', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("Viewing all Favorite Questions by User Jet, that has none saved")
        print(data)
        print(response)
        self.assertEqual(400, response.status_code)
        print("**************************************************\n")

        # View All As Favorited: ---------------------------------------------------
        print("View all favorite answers.")
        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username1 + ":" + "siddiqua", 'ascii')).decode('ascii')}

        response = self.app.post('/api/view/favA', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("Favorite answers of User Salma: ")
        print(data)
        print(response)
        self.assertEqual(200, response.status_code)
        print("\n")

        headers = {'content-type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(bytes(username3 + ":" + "cakes", 'ascii')).decode('ascii')}

        response = self.app.post('/api/view/favA', headers=headers, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print("View favorite answers of jet, which is none since none were added.")
        print(data)
        print(response)
        self.assertEqual(400, response.status_code)
        print("************************************************\n")

    # View all questions and corresponding answers----------------------------
        print("View all questions and corresponding answers.\n")
        response = self.app.post('/api/view/allQA', headers={'content-type': 'application/json'}, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print(data)
        print(response)
        self.assertEqual(200, response.status_code)
        print("************************************************\n")
    # View all questions-----------------------------------------------------
        print("View all questions. \n")
        response = self.app.post('/api/view/allQ', headers={'content-type': 'application/json'}, data=AInfo1)
        data = json.loads(response.get_data(as_text=True))
        print(data)
        print(response)
        self.assertEqual(200, response.status_code)