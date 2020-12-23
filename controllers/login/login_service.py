from flask_jwt_extended import create_access_token, create_refresh_token

from common.key_builder import KeyBuilder
from common.response_builder import ResponseBuilder


def login_service(request_form, users):
    user = users.find_one({"email": request_form["email"]})
    if user is None:
        return ResponseBuilder.failure("User not found", 404)

    if not user['email_confirmed']:
        return ResponseBuilder.failure("Email not confirmed", 401)

    key = KeyBuilder.make_key(salt=user['salt'], password=request_form['password'])

    if key == user["key"]:
        access_token = create_access_token(identity=request_form['email']),
        refresh_token = create_refresh_token(identity=request_form['email'])
        return ResponseBuilder.success({"access_token": access_token, "refresh_token": refresh_token})
    else:
        return ResponseBuilder.failure("Incorrect password", 401)
