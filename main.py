from src.server.instance import server
from flask import jsonify
from blocklist import BLOCKLIST
from db import db
from os import environ
from flask_jwt_extended import JWTManager
from src.controllers.users import Users, UserRegister, UserLogin, UserLogout
from flask_cors import CORS


app, api = server.app, server.api

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL_SITE").replace('postgres://', 'postgresql://')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")
app.config["JWT_BLACKLIST_ENABLED"] = True

db.init_app(app)

@app.before_first_request
def create_db():
  db.create_all()

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def verify_token_in_blocklist(jwt_header, jwt_payload):
  jti = jwt_payload["jti"]
  token_in_blocklist = BLOCKLIST.get_from_blocklist(jti)
  return token_in_blocklist is not None


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
  return jsonify({"message": "You have been logged out."}), 401

'''Resources'''
api.add_resource(Users, '/users/<int:id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
  server.run()
