from flask_restful import Resource, reqparse
from models.users import UsersModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blocklist import BLOCKLIST


class Users(Resource):
  @jwt_required()
  def get(self, id):
    user = UsersModel.find_by_id(id)
    if user:
      return user.json()
    return {'message': 'User not found'}, 404

  def put(self, id):
    params = reqparse.RequestParser()
    params.add_argument('username', type=str)
    params.add_argument('password', type=str)
    params.add_argument('email', type=str)
    params.add_argument('name', type=str)

    data = params.parse_args()
    user = UsersModel.find_by_id(id)
    if user:
      user.update(**data)
      user.save()
      return user.json()
    return {'message': 'User not found'}, 404

  def delete(self, id):
    user = UsersModel.find_by_id(id)
    if user:
      user.delete()
      return {'message': 'User deleted'}
    return {'message': 'User not found'}, 404


class UserRegister(Resource):

  def post(self):
    params = reqparse.RequestParser()
    params.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    params.add_argument('password', type=str, required=True, help="This field cannot be left blank!")
    params.add_argument('email', type=str, required=True, help="This field cannot be left blank!")
    params.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
    data = params.parse_args()
    if UsersModel.find_by_username(data['username']):
      return {'message': 'User {} already exists'.format(data['username'])}, 400

    user = UsersModel(username=data['username'], password=generate_password_hash(data['password']), email=data['email'], name=data['name'])
    try:
      user.save()
    except:
      return {'message': 'An error occurred while creating the user'}, 500
    return user.json(), 201


class UserLogin(Resource):

  def post(self):
    params = reqparse.RequestParser()
    params.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    params.add_argument('password', type=str, required=True, help="This field cannot be left blank!")
    data = params.parse_args()
    user = UsersModel.find_by_username(data['username'])
    if user and check_password_hash(user.password, data['password']):
      access_token = create_access_token(identity=user.id)
      return {'access_token': access_token}, 200
    return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
  @jwt_required()
  def post(self):
    jti = get_jwt()['jti']
    BLOCKLIST.add_to_blocklist(jti)
    return {'message': 'Successfully logged out'}, 200
