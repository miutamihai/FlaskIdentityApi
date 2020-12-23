from flask_jwt_extended import get_jwt_identity

from common.key_builder import KeyBuilder
from common.response_builder import ResponseBuilder


def confirm_service(request_form, users):
    try:
        email = get_jwt_identity()
        if users.find_one({"email": email})["email_confirmed"]:
            return ResponseBuilder.failure("Email already confirmed", 401)
        salt = KeyBuilder.make_salt()
        key = KeyBuilder.make_key(salt, request_form['password'])
        users.update_one({"email": email}, {"$set": {
            "email_confirmed": True,
            "salt": salt,
            "key": key
        }})
        return ResponseBuilder.success({"message": "Email confirmed"})
    except Exception as e:
        return ResponseBuilder.failure(str(e))
