from flask import Response


class ResponseBuilder:
    @staticmethod
    def success(data):
        message = ''
        for key, value in data.items():
            message += f'"{key}": "{value}",'
        message = message[:-1]  # Removes last comma from message
        return Response(f'{{ "success": true, {message} }}', status=200, mimetype='application/json')

    @staticmethod
    def failure(exception, status=500):
        return Response(f'{{ "success": false, "exception": {exception} }}', status=status, mimetype='application/json')
