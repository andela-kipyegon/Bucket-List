
from datetime import datetime

from flask import g, Blueprint, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPTokenAuth
from models import BucketList, BucketListItem, Users
from app import app, db

auth = HTTPTokenAuth(scheme='Token')

# field marshals for the bucketlist items

bucket_list_item_field = {'bucketlist_item_id': fields.Integer,
                          'name': fields.String,
                          'created_at': fields.DateTime,
                          'updated_at': fields.DateTime(dt_format='rfc822'),
                          'done': fields.String
                         }

# field marshals

bucket_list_field = { 'id': fields.Integer,
                      'name': fields.String,
                      'items': fields.Nested(bucket_list_item_field),
                      'created_at': fields.DateTime(dt_format='rfc822'),
                      'updated_at': fields.DateTime(dt_format='rfc822'),
                      'created_by': fields.String,
                      'uri':fields.Url('bucket_list.bucketlist'),
                    }

bucket_list_blueprint = Blueprint('bucket_list', __name__)
api_bucket_list = Api(bucket_list_blueprint)

@auth.verify_token
def verify_token(token):
    """"token authentication"""

    # authenticate by token
    user = Users.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

class BucketListAPI(Resource):
    """ bucket list API """

    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No buckelist name provided',
                                   location='json')
        super(BucketListAPI, self).__init__()

    def get(self, id=None):
        """ fxn for get request of bucketlist or bucketlists """

        if id:
            user_id = g.user.id
            bucket_list = BucketList.query.filter_by(id=id, created_by=user_id).all()
            if bucket_list:
                return marshal(bucket_list, bucket_list_field), 200

            return {'error':'bucket list does not exist'}, 404
        else:
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument('page', location="args", type=int, required=False, default=1)
            self.reqparse.add_argument('per_page', location="args", type=int, default=20)
            self.reqparse.add_argument('q', location="args", required=False)

            args = self.reqparse.parse_args()
            search = args['q']
            page = args['page']
            per_page = args['per_page']
            user_id = g.user.id

            # search if parameter is given
            if search:
                bucket_list = (BucketList.query.filter(BucketList.created_by == user_id,
                                                       BucketList.name.like('%' + search + '%')).
                               paginate(page, per_page, False))
            else:
                bucket_list = BucketList.query.filter_by(created_by=user_id).\
                              paginate(page, per_page, False)

            # bucket list is found
            if not bucket_list:
                return {'message': 'no bucket_list available'}, 404

            if bucket_list.has_next:
                url_next = request.url + '?page='+ str(page + 1) + '&limit=' + str(per_page)
            else:
                url_next = 'Null'

            if bucket_list.has_prev:
                url_prev = request.url + '?page='+ str(page - 1) + '&limit=' + str(per_page)
            else:
                url_prev = 'Null'

            return {'meta':{'next_page':url_next,
                            'previous_page':url_prev,
                            'total_pages': bucket_list.pages},
                    'bucketlist':marshal(bucket_list.items, bucket_list_field)}, 200


    def post(self):
        """ Adds a bucketlist """

        args = self.reqparse.parse_args()
        name = args['name']

        bucket_list = BucketList.query.filter_by(name=name, created_by=g.user.id).first()

        if bucket_list:
            return {'message':'bucketlist {0} already exists'.format(name)}, 202

        new_bucket_list = BucketList(name=name, created_by=g.user.id)
        db.session.add(new_bucket_list)
        db.session.commit()

        return marshal(new_bucket_list, bucket_list_field), 201

    def put(self, id):
        """ updates the bucketlist item of a specific id"""

        args = self.reqparse.parse_args()
        name = args['name']

        bucket_list = BucketList.query.filter_by(id=id, created_by=g.user.id).first()

        if not bucket_list:
            return {'error':'bucketlist does not exists'}, 404

        bucket_list.name = name
        db.session.commit()

        return marshal(bucket_list, bucket_list_field), 200

    def delete(self, id):
        """ deletes bucketlist item of a particular id """

        bucket_list = BucketList.query.filter_by(id=id, created_by=g.user.id).first()

        if bucket_list:
            db.session.delete(bucket_list)
            db.session.commit()

            return {'message':'bucket list {0} deleted successfully'.format(bucket_list.name)}, 200

        return {'message':'bucket list does not exist'}, 404

class BucketListItemAPI(Resource):
    """ API endpoint for the bucketlist item"""

    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(BucketListItemAPI, self).__init__()

    def post(self, bucketlist_id):
        """ creates a new bucketlist item"""

        self.reqparse.add_argument('item_name', type=str, required=True,
                                   help='No item name provided',
                                   location='json')
        args = self.reqparse.parse_args()
        name = args['item_name']
        bucket_list = BucketList.query.filter_by(id=bucketlist_id, created_by=g.user.id).first()

        if bucket_list:
            bucket_list_item = (BucketListItem.query.filter_by(
                bucketlist_id=bucketlist_id, name=name)).first()

            if bucket_list_item:
                return {'message':'item already exists'}, 202

            bucket_list_item_last = (BucketListItem.query.filter_by(bucketlist_id=bucketlist_id)
                                     .order_by(db.desc(BucketListItem.bucketlist_item_id)))

            try:
                last_item_id = bucket_list_item_last[0].bucketlist_item_id
            except IndexError:
                last_item_id = 0


            bucket_list_item = BucketListItem(bucketlist_id=bucketlist_id, name=name,\
                bucketlist_item_id=last_item_id + 1)
            db.session.add(bucket_list_item)
            db.session.commit()
            return marshal(bucket_list_item, bucket_list_item_field), 201

        return {'error':'bucket list cannot be found'}, 404

    def put(self, bucketlist_id, bucketlist_item_id):
        """
        updates a particular bucketlist item of  a particular id
        """

        self.reqparse.add_argument('done', type=bool,
                                   help='No done argument provided',
                                   location='json')
        self.reqparse.add_argument('item_name', type=str,
                                   help='No item name provided',
                                   location='json')
        args = self.reqparse.parse_args()
        name = args['item_name']
        done = args['done']

        bucket_list = BucketList.query.filter_by(id=bucketlist_id, created_by=g.user.id).first()

        if not bucket_list:
            return {'error':'bucket list does not exist'}, 404

        bucket_list_item = BucketListItem.query.\
                                    filter_by(bucketlist_item_id=bucketlist_item_id,\
                                      bucketlist_id=bucketlist_id).first()

        if not bucket_list_item:
            return {'error':'bucket list item does not exist'}, 404

        if name:
            bucket_list_item.name = name

        if done:
            bucket_list_item.done = done

        db.session.commit()
        return marshal(bucket_list_item, bucket_list_item_field), 200

    def delete(self, bucketlist_id, bucketlist_item_id):
        """ deletes a particular bucket list item"""

        bucket_list = BucketList.query.filter_by(id=bucketlist_id,\
                                                created_by=g.user.id).first()

        if not bucket_list:
            return {'message':'bucket list does not exist'}, 404

        bucket_list_item = BucketListItem.query.filter_by(id=bucketlist_item_id).first()

        if not bucket_list_item:
            return {'message':'bucket list item does not exist'}, 404

        db.session.delete(bucket_list_item)
        db.session.commit()
        return {'message':'bucket list item deleted'}, 200



api_bucket_list.add_resource(BucketListItemAPI, '/bucketlist/<int:bucketlist_id>/bucketlistitem/',\
                                                             endpoint='create_bucketlistitem')
api_bucket_list.add_resource(BucketListItemAPI,\
                            '/bucketlist/<int:bucketlist_id>/bucketlistitem/'+
                             '<int:bucketlist_item_id>/',
                             endpoint='bucketlistitem')
(api_bucket_list.add_resource(BucketListAPI, '/bucketlist/',
                              '/bucketlist/<int:id>', endpoint='bucketlist'))
