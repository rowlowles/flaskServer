from flask import Flask
from flask_restplus import Resource, Api, fields
from database import db_session
from models import cardInfo

app = Flask(__name__)
api = Api(app,
          version='0.1',
          title='cardobot API',
          description='Simple API for the carobot sorter'
          )


@api.route('/welcome')
class BaseRoute(Resource):
    def get(self):
        return {'Message': 'Welcome to the cardobot API!'}


@api.route('/cardInfo')
class cardInfo(Resource):
    model = api.model('Model', {
        'id': fields.String,
        'name': fields.String,
        'setName': fields.String,
        'typeLine': fields.String,
        'blue': fields.Integer,
        'green': fields.Integer,
        'white': fields.Integer,
        'black': fields.Integer,
        'red': fields.Integer,
        'price': fields.Integer,
        'lastUpdated': fields.DateTime,
        'foilPrice': fields.Integer,
        'tcgIdNumber': fields.Integer,
        })
    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return cardInfo.query.all()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(debug=True)
