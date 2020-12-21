from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_mail import Mail, Message

import uuid

from arguments import Arguments
from config import Config

ARGS = Arguments.parse()

app = Config.with_args(Flask(__name__), ARGS)

mail = Mail(app)
jwt = JWTManager(app)


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@app.route('/register', methods=['POST'])
def register():
    confirmation_id = uuid.uuid1()
    msg = Message('Bun venit de la LexBox', sender=ARGS.email, recipients=[request.form['email']])
    msg.html = render_template("ConfirmationEmail.html",
                               firstName=request.form['firstName'],
                               lastName=request.form['lastName'],
                               confirmationUrl=f'http://localhost:5000/confirm_email/{confirmation_id}')
    mail.send(msg)
    return "Sent"


@app.route('/confirm_email/<uuid:confirmation_id>', methods=['POST', 'GET'])
def confirm(confirmation_id):
    return str(confirmation_id)


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run()
