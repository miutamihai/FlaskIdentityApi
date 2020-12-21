import os


class Config:
    @staticmethod
    def for_app(app):
        app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
        app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        return app
