from flask_restful import Resource, marshal, reqparse, fields
from app.utils import QueryChk
from app.models import db, Author, AuthorType, ToDo


class EnumItem(fields.Raw):
   def format(self, enum):
      try:
           return enum.value
      except:
          return None


class EnumChk(object):
    def __init__(self, _enum):
        self.enum = _enum

    def __call__(self, value):
        if value not in self.enum.__members__.keys():
            message = 'Value does not member of Enum: {0}'.format(self.enum.__name__)
            raise ValueError(message)
        return self.enum[value]

    def __deepcopy__(self, memo):
        return EnumChk(self.enum)


class AuthorApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True)
        self.parser.add_argument('type', type=EnumChk(AuthorType))

        self.fields = {
            'id': fields.Integer,
            'name': fields.String,
            'type': EnumItem
        }

        super(AuthorApi, self).__init__()

    def get(self, id):
        author = Author.query.get_or_404(id)
        return marshal(author, self.fields, envelope='author')

    def put(self, id):
        author = Author.query.get_or_404(id)
        args = self.parser.parse_args()
        author.update(args)
        print(author.name)
        try:
            db.session.commit()
            return {'success': 'Author "{0}" was updated!'.format(author.name)}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def delete(self, id):
        author = Author.query.get_or_404(id)
        try:
            db.session.delete(author)
            db.session.commit()
            return '', 204
        except Exception as e:
            return {'error': str(e)}, 500


class AuthorListApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        filtrable = {
            "name": {
                "type": str,
                "ops": ['eq', 'lk']
            },
            "type": {
                "type": EnumChk(AuthorType),
                "ops": ['eq']
            }
        }
        self.parser.add_argument('q', required=False, type=QueryChk(filtrable))

    def get(self):
        args = self.parser.parse_args()
        return args['q']

    def post(self):
        pass