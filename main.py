import os
import uuid

from flask import jsonify, request, render_template
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from flask_mail import Message

from config.setup import setup

app, mail, jwt, users = setup()


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
    email = request.form['email']
    msg = Message('Bun venit de la LexBox', sender=os.getenv('EMAIL'), recipients=[email])
    msg.html = render_template("ConfirmationEmail.html",
                               firstName=request.form['firstName'],
                               lastName=request.form['lastName'],
                               confirmationUrl=f'{os.getenv("URL")}/confirm_email/{confirmation_id}?email={email}')
    mail.send(msg)
    users.insert_one({
        "firstName": request.form['firstName'],
        "lastName": request.form['lastName'],
        "email": email
    })
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
