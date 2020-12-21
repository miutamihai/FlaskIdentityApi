class Config:
    @staticmethod
    def with_args(app, args):
        app.config['JWT_SECRET_KEY'] = args.secret
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = args.email
        app.config['MAIL_PASSWORD'] = args.password
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        return app
