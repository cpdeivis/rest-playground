from typing import List, Any, Optional
from flask_sqlalchemy.model import DefaultMeta


class Operator(object):
    lookup = None
    label = None

    def __call__(self, model: DefaultMeta, attr: str, value: Any):
        column = getattr(model, attr)
        condition = getattr(column, self.lookup)(value)
        return condition


class Equal(Operator):
    lookup = '__eq__'
    label = 'eq'


class NotEqual(Operator):
    lookup = '__ne__'
    label = 'ne'


class GreaterThan(Operator):
    lookup = '__gt__'
    label = 'gt'


class GreaterEqual(Operator):
    lookup = '__ge__'
    label = 'ge'


class LessThan(Operator):
    lookup = '__lt__'
    label = 'lt'


class LessEqual(Operator):
    lookup = '__le__'
    label = 'le'


class Like(Operator):
    lookup = 'like'
    label = 'lk'

    def __call__(self, model: DefaultMeta, attr: str, value: Any):
        return super(Like, self).__call__(model, attr, "%{0}%".format(value))


class ILike(Operator):
    lookup = 'ilike'
    label = 'ik'

    def __call__(self, model: DefaultMeta, attr: str, value: Any):
        return super(ILike, self).__call__(model, attr, "%{0}%".format(value))


def available_operators() -> List[str]:
    return [getattr(x, 'label') for x in Operator.__subclasses__()]


def get_operator(label: str) -> Optional[Operator]:
    return next((x for x in Operator.__subclasses__() if getattr(x, 'label') == label), None)
