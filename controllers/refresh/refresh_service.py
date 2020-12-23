from flask_jwt_extended import get_jwt_identity, create_access_token

from common.response_builder import ResponseBuilder


def refresh_service():
    email = get_jwt_identity()
    access_token = create_access_token(identity=email)
    return ResponseBuilder.success({"access_token": access_token})
