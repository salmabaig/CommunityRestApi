#!/usr/bin/env python
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_restful import Resource, Api
import simplejson

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
api = Api(app)
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

class favQ(db.Model): # define question model
    __tablename__ = 'favQ'
    user_Id = db.Column(db.String(64), primary_key=True)
    qID = db.Column(db.Integer, primary_key=True)

# defining a row for adding favorite answers
class favA(db.Model): # define question model
    __tablename__ = 'favA'
    user_Id = db.Column(db.String(64),primary_key=True)
    aID = db.Column(db.Integer,primary_key=True)

# defining a row for adding answers to questions
class Answers(db.Model): # define question model
    __tablename__ = 'Answers'
    a_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(140), index=True)
    user_Id = db.Column(db.String(64))
    qID = db.Column(db.Integer)

# defining a row for adding a question
class Questions(db.Model): # define question model
    __tablename__ = 'questions'
    q_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(140), index=True)
    userId = db.Column(db.String(64))

# defining a row for adding a user
class User(db.Model): # define user model
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password): # Hashing pwd, from passlib pkg
        self.password_hash = pwd_context.encrypt(password) # stores hash of usr

    def verify_password(self, password): #Validate the password
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

class CreateNewUser(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            abort(400,"No UserName/Password entered")    # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            abort(400, "User exists")    # existing user
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return (jsonify({'username': user.username}))

# Posting questions for other users.
class CreateNewQuestion(Resource):
    @auth.login_required
    def post(self):
        question = request.json.get('question')
        if question is None:
            abort(400, "Question is not included")    # missing arguments
        new_quest = Questions(question=question, userId = g.user.id)
        db.session.add(new_quest)
        db.session.commit()
        return (jsonify({'question': new_quest.question}))

# Answer questions posted by others.
class CreateNewAnswer(Resource):
    @auth.login_required
    def post(self):
        answer = request.json.get('answer')
        qID = request.json.get('q_id')
        if answer is None or qID is None:
            abort(400, "No answer or qID entered")    # missing arguments
        new_ans = Answers(answer=answer, user_Id = g.user.id,qID = qID)
        db.session.add(new_ans)
        db.session.commit()
        return (jsonify({'answer': new_ans.answer}))

# Add favorite question
class AddFaveQ(Resource):
    @auth.login_required
    def post(self):
        q_ID = request.json.get('q_id')
        if favQ.query.filter_by(user_Id=g.user.id, qID=q_ID).first() is not None:
            abort(400, "You already have this question in favorites.")
        if q_ID is None or Questions.query.filter_by(q_id=q_ID).first() is None:
            abort(400, "Invalid q_id/No q_id")
        new_favQ = favQ(qID = q_ID, user_Id = g.user.id)
        db.session.add(new_favQ)
        db.session.commit()
        return (jsonify({'question': new_favQ.qID}))

class AddFaveA(Resource):
    @auth.login_required
    def post(self):
        a_ID = request.json.get('a_id')
        if favA.query.filter_by(user_Id=g.user.id, aID=a_ID).first() is not None:
            abort(400,"You already have this answer in favorites")
        if a_ID is None or Answers.query.filter_by(a_id=a_ID).first() is None:
            abort(400, "Invalid a_id/No a_id included")
        new_favA = favA(aID = a_ID, user_Id = g.user.id)
        db.session.add(new_favA)
        db.session.commit()
        return (jsonify({'answer': new_favA.aID}))

# View favorite answers
class ViewFaveA(Resource):
    @auth.login_required
    def post(self):
        new_favA = favA.query.filter_by(user_Id=g.user.id).all()
        if favA.query.filter_by(user_Id=g.user.id).first() is None:
            abort(400, "No Favorite Answers")
        favA_dict = []

        for row in new_favA:
            retAnswer = Answers.query.filter_by(a_id = row.aID).first()
            fave = {'a_id': row.aID, "Answer" : retAnswer.answer}
            favA_dict.append(fave)
        return simplejson.dumps(favA_dict)

# View favorite answers
class ViewFaveQ(Resource):
    @auth.login_required
    def post(self):
        new_favQ = favQ.query.filter_by(user_Id=g.user.id).all()
        if favQ.query.filter_by(user_Id=g.user.id).first() is None:
            abort(400, "No Favorites Questions")
        favQ_dict = []

        for row in new_favQ:
            retQ = Questions.query.filter_by(q_id = row.qID).first()
            fave = {'q_id': row.qID, "Question" : retQ.question}
            favQ_dict.append(fave)
        return simplejson.dumps(favQ_dict)

# View all Questions and Responses.
class ViewQA(Resource):
    def post(self):
        allQ = Questions.query.all()
        if allQ is None:
            abort(400, "No Questions have been asked.")
        Q_dict = []

        for row in allQ:
            retA = Answers.query.filter_by(qID= row.q_id).all()
            if Answers.query.filter_by(qID= row.q_id).first() is None:
                fave = {'q_id': row.q_id, "Question": row.question}
                Q_dict.append(fave)
            else:
                for each in retA:
                    Q_dict.append({'q_id': row.q_id, "Question": row.question, "Answer" : each.answer})
        return simplejson.dumps(Q_dict)

# View all Questions.
class ViewQ(Resource):
    def post(self):
        allQ = Questions.query.all()
        if allQ is None:
            abort(400, "No Questions have been asked.")
        Q_dict = []
        for row in allQ:
            fave = {'q_id': row.q_id, "Question": row.question}
            Q_dict.append(fave)
        return simplejson.dumps(Q_dict)

class Token(Resource):
    @auth.login_required
    def post(self):
        token = g.user.generate_auth_token(600)
        return jsonify({'token': token.decode('ascii'), 'duration': 600})

api.add_resource(CreateNewUser, '/api/users')
api.add_resource(CreateNewQuestion, '/api/questions')
api.add_resource(CreateNewAnswer, '/api/answers')
api.add_resource(AddFaveQ, '/api/favQ')
api.add_resource(AddFaveA, '/api/favA')
api.add_resource(ViewFaveA, '/api/view/favA')
api.add_resource(ViewFaveQ, '/api/view/favQ')
api.add_resource(ViewQA, '/api/view/allQA')
api.add_resource(ViewQ, '/api/view/allQ')
api.add_resource(Token, '/api/token')

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)