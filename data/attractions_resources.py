import os
import datetime
from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.attractions import Attractions


def abort_if_attractions_not_found(attractions_id):
    session = db_session.create_session()
    atttractions = session.query(Attractions).get(attractions_id)
    if not atttractions:
        abort(404, message=f'Attractions {attractions_id} not found')


class AttractionsResource(Resource):
    def get(self, attractions_id):
        abort_if_attractions_not_found(attractions_id)
        session = db_session.create_session()
        attractions = session.query(
            Attractions).get(attractions_id)
        return jsonify({'attractions': attractions.to_dict(
            only=('name',
                  'description',
                  'city',
                  'map',
                  'pic',
                  'created_date',
                  'user_id')
        )})

    def delete(self, attractions_id):
        abort_if_attractions_not_found(attractions_id)
        session = db_session.create_session()
        attractions = session.query(Attractions).get(attractions_id)
        if os.path.isfile(f'static/img/{attractions.name}.jpg'):
            os.remove(f'static/img/{attractions.name}.jpg')
        session.delete(attractions)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('description', required=True)
parser.add_argument('city', required=True)
# parser.add_argument('map', required=True)
# parser.add_argument('pic', required=True)
parser.add_argument('user_id', required=True, type=int)


class AttractionsListResourse(Resource):
    def get(self):
        session = db_session.create_session()
        attractions = session.query(Attractions).all()
        return jsonify({'attractions': [item.to_dict(
            only=(
                'name',
                'description',
                'city',
                'map',
                'pic',
                'created_date',
                'user_id'
                )) for item in attractions]
        })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        attractions = Attractions(
            name=args['name'],
            description=args['description'],
            city=args['description'],
            user_id=args['user_id'],
            map=f"https://yandex.ru/maps/?mode=search&text={args['name']}",
            created_date=datetime.datetime.now()
        )
        session.add(attractions)
        session.commit()
        return jsonify({'id': attractions.id})
