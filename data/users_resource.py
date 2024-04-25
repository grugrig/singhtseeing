import datetime
from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.users import User


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f'User {user_id} not found')


class UserResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'news': user.to_dict(
            only=('id',
                  'name',
                  'sex',
                  'age',
                  'about',
                  'email',)
        )})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('sex', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('about', required=True)
parser.add_argument('email', required=True)


class UsersListResourse(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id',
                  'name',
                  'sex',
                  'age',
                  'about',
                  'email')
                  ) for item in users]
        })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            sex=args['sex'],
            age=args['age'],
            about=args['about'],
            email=args['email'],
            created_date=datetime.datetime.now()
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})
