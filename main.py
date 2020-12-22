import hashlib
import os

from docxtpl import DocxTemplate
from flask import request, render_template, Response
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from flask_mail import Message

from config.setup import setup

app, mail, jwt, users = setup()


@app.route('/login', methods=['POST'])
def login():
    user = users.find_one({"email": request.form["email"]})
    if user is None:
        return Response('{ "success": false, "exception": "User not found" }', status=404, mimetype='application/json')

    key = hashlib.pbkdf2_hmac(
        'sha256',
        request.form['password'].encode('utf-8'),
        user["salt"],
        100000
    )

    if key == user["key"]:
        access_token = create_access_token(identity=request.form["email"])
        return Response(f'{{ "success": true, "token": "{access_token}" }}', status=200, mimetype='application/json')
    else:
        return Response('{ "success": false, "exception": "Incorrect password" }', status=401, mimetype='application'
                                                                                                        '/json')


@app.route('/register', methods=['POST'])
def register():
    try:
        email = request.form['email']
        if users.find_one({"email": email}) is not None:
            return Response('{ "success": false, "exception": "Email already exists" }', status=401, mimetype='application/json')
        msg = Message('Bun venit de la LexBox', sender=os.getenv('EMAIL'), recipients=[email])
        msg.html = render_template("ConfirmationEmail.html",
                                   firstName=request.form['firstName'],
                                   lastName=request.form['lastName'],
                                   confirmationUrl=f'{os.getenv("URL")}/confirm_email?email={email}')
        mail.send(msg)
        users.insert_one({
            "firstName": request.form['firstName'],
            "lastName": request.form['lastName'],
            "email": email,
            "cnp": request.form['cnp'],
            "ci": {
                "series": request.form['ciSeries'],
                "number": request.form['ciNumber']
            },
            "email_confirmed": False,
            "address": {
                "city": request.form['city'],
                "street": request.form['street'],
                "number": request.form['number'],
                "block": request.form['block'],
                "stair": request.form['stair'],
                "apartment": request.form['apartment'],
                "county": request.form['county']
            }
        })
        access_token = create_access_token(identity=email)
        return Response(f'{{ "success": true, "token": "{access_token}" }}', status=200, mimetype='application/json')
    except Exception as e:
        return Response(f'{{ "success": false, "exception": {str(e)} }}', status=500, mimetype='application/json')


@app.route('/confirm_email', methods=['POST'])
@jwt_required
def confirm():
    try:
        email = get_jwt_identity()
        if users.find_one({"email": email})["email_confirmed"]:
            return Response('{ "success": false, "exception": Email already confirmed }', status=401, mimetype='application/json')
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
        return Response('{ "success": true }', status=205, mimetype='application/json')
    except Exception as e:
        return Response(f'{{ "success": false, "exception": {str(e)} }}', status=500, mimetype='application/json')


@app.route('/generate_document', methods=['POST'])
@jwt_required
def generate():
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
        "fine": request.json.get('fine', None)
    }
    doc.render(context)
    doc.save("result.docx")
    return Response('', status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()
