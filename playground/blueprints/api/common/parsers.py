from .operators import get_operator
import re


class QueryChk(object):
    def __init__(self, searchable, query, model=None):
        self.searchable = searchable
        self.query = query
        self.model = model if model else query.column_descriptions[0]['type']

    def __call__(self, value):
        re_query = re.compile(r'^(\[(([A-Za-z]+):([a-z]{2})=([A-Za-z0-9-]+),?)+\])$')
        re_op = re.compile(r'([A-Za-z]+:[a-z]{2}=[A-Za-z0-9-]+)')

        if not re_query.search(value):
            message = 'Query is not in right format!'
            raise ValueError(message)

        # list of search operations from web args
        req_ops = re_op.findall(value)
        # list of conditions in SQLAlchemy Expression format
        conditions = [self._make_condition(x) for x in req_ops]

        q_aux = self.query.filter(*conditions)
        # dummy swap of objects content
        self.query.__dict__ = q_aux.__dict__
        del q_aux

        return value

    def __deepcopy__(self, memo):
        return QueryChk(self.searchable, self.query, self.model)

    def _make_condition(self, web_arg: str):
        op_txt = re.split(r':|=', web_arg)
        if op_txt[0] in self.searchable:
            field = self.searchable.get(op_txt[0])
            if op_txt[1] in field['ops']:
                try:
                    return get_operator(op_txt[1])()(self.model, op_txt[0], field['type'](op_txt[2]))
                except TypeError:
                    message = 'The value "{0}" is not in right format to field "{1}". ' \
                              'The field expect a "{2}" value!'.format(op_txt[2], op_txt[0], field['type'].__name__)
                    raise ValueError(message)
            else:
                message = 'The "{0}" is not a allowed operation to field "{1}"!'.format(op_txt[1], op_txt[0])
                raise ValueError(message)
        else:
            message = 'The field "{0}" is not searchable!'.format(op_txt[0])
            raise ValueError(message)


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
