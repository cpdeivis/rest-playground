from .common.base import SingleR, ListR, Argument, fields
from .common.parsers import EnumChk
from playground.models import db, Author, AuthorType, ToDo


class EnumItem(fields.Raw):
    def format(self, enum):
        try:
            return enum.value
        except:
            return None


class AuthorApi(SingleR):
    def __init__(self):
        ps = [Argument('name', type=str, required=True), Argument('type', type=EnumChk(AuthorType))]
        fs = {
            'id': fields.Integer,
            'name': fields.String,
            'type': EnumItem
        }

        super(AuthorApi, self).__init__(ps, fs, 'author')

    def get(self, id):
        author = Author.query.get_or_404(id)
        return author

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


class AuthorListApi(ListR):
    def __init__(self):
        searchable = {
            "name": {
                "type": str,
                "ops": ['eq', 'ik'],
            },
            "type": {
                "type": EnumChk(AuthorType),
                "ops": ['eq'],
            }
        }
        fs = {
            'id': fields.Integer,
            'name': fields.String,
            'type': EnumItem
        }
        super(AuthorListApi, self).__init__(Author.query, searchable=searchable, fs=fs, envelope='authors')

    def get(self):
        self.get_parser.parse_args()
        authors = self.query.all()
        return authors

    def post(self):
        pass
