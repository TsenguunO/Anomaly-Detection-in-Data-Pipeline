from flask import Blueprint
from flask_restx import Api, Resource, fields
from flask import request, jsonify
from datetime import datetime, timezone

from app.db_models.table_classes import Credentials, UserLog, SecurityQuestion, QuestionName
from app.extensions import db

user_api_blueprint = Blueprint('user_api', __name__)
api = Api(user_api_blueprint, doc='/')


Auth_namespace = api.namespace('Authentication', description='User Authentication description')

user_model = api.model('user_model', {
    'email': fields.String(required=True, description="The user's email"),
    'password': fields.String(required=True, description='The user password')
})

signup_model = api.model('signup_model', {
    'email': fields.String(required=True, description="The user's email"),
    'password': fields.String(required=True, description='The user password'),
    'question_id_1': fields.Integer(required=True, description='The selected security question ID'),
    'answer_1': fields.String(required=True, description='The answer to the security question'),
    'question_id_2': fields.Integer(required=True, description='The selected security question ID'),
    'answer_2': fields.String(required=True, description='The answer to the security question')
})

password_model = api.model('password_model', {
    'email': fields.String(required=True, description="The user's email"),
    'old_password': fields.String(required=True, description='The user old password'),
    'new_password': fields.String(required=True, description='The user new password')
})

forget_password_model = api.model('forget_password_model', {
    'email': fields.String(required=True, description="The user's email"),
    'answer_to_1st_q': fields.String(required=True, description='The answer to the security question'),
    'answer_to_2nd_q': fields.String(required=True, description='The answer to the security question'),
    'new_password': fields.String(required=True, description='The user new password')
})

user_log_model = api.model('user_log_model', {
    'user_id_fk': fields.Integer(required=True, description="The user's id")
})

def password_strength(password):
    length = len(password) >= 8
    lowercase = any(char.islower() for char in password)
    uppercase = any(char.isupper() for char in password)
    digit = any(char.isdigit() for char in password)
    special = any(char in '!@#$%^&*()-_=+[{]}\|;:\'",<.>/?' for char in password)

    if length and lowercase and uppercase and digit and special:
        return "Strong"
    else:
        return "Weak"

@Auth_namespace.route('/GetAllQuestions')
class Questions(Resource):
    def get(self):
        """Get all available security questions"""
        questions = QuestionName.query.all()
        if not questions:
            return {"error": "No questions found"}, 404
        questions_dict = {question.id: question.question for question in questions}
        return jsonify(questions_dict)
    
@Auth_namespace.route('/signup')
class Signup(Resource):
    @Auth_namespace.expect(signup_model)
    def post(self):
        """Please use 'GetAllQuestions' to see all questions first and then choose """
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        question_id_1 = data.get('question_id_1')
        answer_1 = data.get('answer_1')
        question_id_2 = data.get('question_id_2')
        answer_2 = data.get('answer_2')
        created_timestamp = datetime.now(timezone.utc)

        if not all([email, password, question_id_1, answer_1, question_id_2, answer_2]):
            return {"error": "Email, password, question_id_1, answer_1, question_id_2, and answer_2 are required"}, 400
        
        q1_res = QuestionName.query.filter_by(id=question_id_1).first()
        q2_res = QuestionName.query.filter_by(id=question_id_2).first()
        if not q1_res:
            return {"error": "Q1 ID does not exist"}, 400
        if not q2_res:
            return {"error": "Q2 ID does not exist"}, 400

        credential_result = Credentials.query.filter_by(email=email).first()
        if credential_result:
            return {"error": "Email is already taken, choose different"}, 401
        if question_id_1 == question_id_2:
            return {"error": "Question choose should be different"}, 401
        if password_strength(password) == "Weak":
            return {"error": "You password doesnot meet security standard, please re-set"}, 401
        else:
            new_user = Credentials(email=email, password=password, created_timestamp=created_timestamp)
            db.session.add(new_user)
            db.session.commit()

            new_security_questions = SecurityQuestion(user_id_fk=new_user.user_id, question_id_1_fk=question_id_1, answer_1=answer_1,
                                                      question_id_2_fk=question_id_2, answer_2=answer_2)
            db.session.add(new_security_questions)
            db.session.commit()

            return {'message': 'User signed up successfully'}, 201


@Auth_namespace.route('/login')
class login(Resource):
    @Auth_namespace.expect(user_model)
    def post(self):

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        log_timestamp = datetime.now(timezone.utc)
        if not email or not password:
            return {"error": "Email and password are required"}, 400
        
        credential_result = Credentials.query.filter_by(email=email, password=password).first()

        if credential_result:
            print(credential_result)
            print(f'user_id = {credential_result.user_id}')
            new_userlog = UserLog(user_id_fk = credential_result.user_id, log_timestamp = log_timestamp)
            db.session.add(new_userlog)
            db.session.commit()
            return {"success": "Logged in successfully"}, 200
        else:
            return {"error": "Email or password is wrong"}, 400
##################
###### Nice to have - 1) Lock user attempts for logging in after 3 wrong attempts

@Auth_namespace.route('/change_password')
class ChangePasswordWithOld(Resource):
    @api.expect(password_model)
    def post(self):
        """Change password by using old password"""
        data = request.get_json()
        email = data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not all([email, old_password, new_password]):
            return {"error": "Email, old_password, and new_password are required"}, 400

        user = Credentials.query.filter_by(email=email).first()
        if not user:
            return {"error": "Email not found"}, 404

        if user.password != old_password:
            return {"error": "Incorrect old password"}, 401

        if old_password == new_password:
            return {"error": "New password cannot be the same as the old password"}, 401

        if password_strength(new_password) == "Weak":
            return {"error": "You password doesnot meet security standard, please re-set"}, 401

        user.password = new_password
        db.session.commit()

        return {"message": "Password updated successfully"}, 200



@Auth_namespace.route('/forget_password/get_questions')
class ChangePasswordWithSecurityQuestions(Resource):
    @api.expect(api.parser().add_argument('email', type=str, required=True))
    def get(self):
        """Get use's security questions"""
        data = request.args
        email = data.get('email')
        if not email:
            return {"error": "Email is required"}, 400
        
        user = Credentials.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 400

        security_questions = SecurityQuestion.query.filter_by(user_id_fk=user.user_id).first()
        if not security_questions:
            return {"error": "Security questions not set for this email"}, 404

        question_id_1 = security_questions.question_id_1_fk
        question_id_2 = security_questions.question_id_2_fk
        questions = []
        for question_id in [question_id_1, question_id_2]:
            question = QuestionName.query.filter_by(id=question_id).first()
            if question:
                questions.append(question.question)

        return {"Your security questions are: ": questions}, 200


@Auth_namespace.route('/forget_password/post_answers')
class ChangePasswordWithSecurityQuestions(Resource):
    @api.expect(forget_password_model)
    def post(self):
        """Change password by answering security question"""
        data = request.get_json()
        email = data.get('email')
        answer_1 = data.get('answer_to_1st_q')
        answer_2 = data.get('answer_to_2nd_q')
        new_password = data.get('new_password')

        user = Credentials.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 400

        if not all([email, answer_1, answer_2]):
            return {"error": "Email and answers are required"}, 400

        security_questions = SecurityQuestion.query.filter_by(user_id_fk=user.user_id).first()
        if not security_questions:
            return {"error": "Security questions not set for this email"}, 401

        if security_questions.answer_1 != answer_1 or security_questions.answer_2 != answer_2:
            return {"error": "Incorrect answers provided"}, 401

        if password_strength(new_password) == "Weak":
            return {"error": "You password doesnot meet security standard, please re-set"}, 401

        user.password = new_password
        db.session.commit()

        return {"message": "Password updated successfully"}, 200