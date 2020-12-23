import os
import uuid

from docxtpl import DocxTemplate
from flask import render_template
from flask_jwt_extended import get_jwt_identity
from flask_mail import Message

from common.response_builder import ResponseBuilder


def build_document_input(user, request_json):
    return {
        "law": request_json.get('law', None),
        "first_name": user['firstName'],
        "last_name": user['lastName'],
        "address": user['address'],
        "ci": user['ci'],
        "assisted": request_json.get('assisted', None),
        "accused": request_json.get('accused', None),
        "record": request_json.get('record', None),
        "fine": request_json.get('fine', None),
        "sanction": request_json.get('sanction', None),
        "agreed_to_sanction": request_json.get('agreed_to_sanction', None),
        "witnesses": request_json.get('witnesses', None)
    }


def generate_service(request_json, users, mail, minio_client, owner_email):
    try:
        doc = DocxTemplate("templates/request.docx")
        user = users.find_one({"email": get_jwt_identity()})
        context = build_document_input(user, request_json)
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
