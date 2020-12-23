import hashlib
import os
import uuid

from docxtpl import DocxTemplate
from flask import request, render_template, Response
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required, create_access_token,
    get_jwt_identity, create_refresh_token
)
from flask_mail import Message

from common.response_builder import ResponseBuilder
from config.setup import setup
from controllers.main import Controller

app, mail, jwt, users, minio_client, owner_email = setup()


@app.route('/login', methods=['POST'])
def login():
    user = users.find_one({"email": request.form["email"]})
    if user is None:
        return ResponseBuilder.failure("User not found", 404)

    key = hashlib.pbkdf2_hmac(
        'sha256',
        request.form['password'].encode('utf-8'),
        user["salt"],
        100000
    )

    if key == user["key"]:
        access_token = create_access_token(identity=request.form['email']),
        refresh_token = create_refresh_token(identity=request.form['email'])
        return ResponseBuilder.success({"access_token": access_token, "refresh_token": refresh_token})
    else:
        return ResponseBuilder.failure("Incorrect password", 401)


@app.route('/register', methods=['POST'])
def register():
    return Controller.register(request_form=request.form, users=users, mail=mail)


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    email = get_jwt_identity()
    access_token = create_access_token(identity=email)
    return ResponseBuilder.success({"access_token": access_token})


@app.route('/confirm_email', methods=['POST'])
@jwt_required
def confirm():
    try:
        email = get_jwt_identity()
        if users.find_one({"email": email})["email_confirmed"]:
            return ResponseBuilder.failure("Email already confirmed", 401)
        salt = os.urandom(32)
        password = request.form['password']
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        users.update_one({"email": email}, {"$set": {
            "email_confirmed": True,
            "salt": salt,
            "key": key
        }})
        return ResponseBuilder.success({"message": "Email confirmed"})
    except Exception as e:
        return ResponseBuilder.failure(str(e))


@app.route('/generate_document', methods=['POST'])
@jwt_required
def generate():
    try:
        doc = DocxTemplate("templates/request.docx")
        user = users.find_one({"email": get_jwt_identity()})
        context = {
            "law": request.json.get('law', None),
            "first_name": user['firstName'],
            "last_name": user['lastName'],
            "address": user['address'],
            "ci": user['ci'],
            "assisted": request.json.get('assisted', None),
            "accused": request.json.get('accused', None),
            "record": request.json.get('record', None),
            "fine": request.json.get('fine', None),
            "sanction": request.json.get('sanction', None),
            "agreed_to_sanction": request.json.get('agreed_to_sanction', None),
            "witnesses": request.json.get('witnesses', None)
        }
        doc.render(context)
        doc.save("result.docx")
        file_name = f'Cerere-{user["firstName"]}-{user["lastName"]}-{str(uuid.uuid1())}.docx'
        with open("result.docx", "rb") as f:
            minio_client.upload_fileobj(f, 'lexbox', file_name)
        os.remove('result.docx')
        download_link = f'http://localhost:9000/lexbox/{file_name}'

        msg = Message('Notificare LexBox', sender=os.getenv('EMAIL'), recipients=[owner_email])
        msg.html = render_template("NotificationEmail.html",
                                   firstName=user['firstName'],
                                   lastName=user['lastName'],
                                   documentUrl=download_link)
        mail.send(msg)
        return ResponseBuilder.success({"download_link": download_link})
    except Exception as e:
        return ResponseBuilder.failure(str(e))


if __name__ == '__main__':
    app.run()
