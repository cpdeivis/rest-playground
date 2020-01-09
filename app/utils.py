import re


class QueryChk(object):
    def __init__(self, filtrable: dict):
        self.re_query = re.compile(r'^(\[(([A-Za-z]+):([a-z]{2})=([A-Za-z0-9-]+)&?)+\])$')
        self.re_op = re.compile(r'([A-Za-z]+:[a-z]{2}=[A-Za-z0-9-]+)')
        self.filtrable = filtrable

    def __call__(self, value):
        if not self.re_query.search(value):
            message = 'Query is not in right format!'
            raise ValueError(message)

        # list of search operations from web args
        req_op = self.re_op.findall(value)
        ops = []
        for op in req_op:
            _op = re.split(r':|=', op)
            if _op[0] in self.filtrable:
                field = self.filtrable.get(_op[0])
                if _op[1] in field['ops']:
                    if self.convert(_op[2], field['type']):
                        ops.append(op)

        return "&".join(ops)

    def __deepcopy__(self, memo):
        return QueryChk(self.filtrable)

    @staticmethod
    def convert(value, stype):
        if value is None:
            return value

        try:
            return stype(value)
        except:
            return None
