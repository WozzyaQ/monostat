import json

from flask import Flask, request, abort
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError

from models import StatementItem
from models import db
from utils import map_from_dict_like


def create_app():
    app = Flask(__name__)
    app.config.from_file('config.json', load=json.load)
    db.init_app(app)

    return app


class WebhookHandler(Resource):

    def post(self):
        try:
            request_data = request.get_json()

            data = request_data['data']
            statement_item = data['statementItem']
            statement_item.update(account=data['account'])
        except KeyError:
            abort(400)

        statement = map_from_dict_like(StatementItem, statement_item)

        try:
            db.session.add(statement)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return 500

        return 200


if __name__ == '__main__':
    app = create_app()
    api = Api(app)
    api.add_resource(WebhookHandler, app.config['WEBHOOK_HANDLER_API_URL'])

    app.run(host='0.0.0.0', debug=True)
