from controllers.register.register_service import register_service


class Controller:
    @staticmethod
    def register(request_form, users, mail):
        return register_service(request_form, users, mail)
