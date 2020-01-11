from typing import List, Optional, Dict
from flask_restful import Resource, reqparse, marshal_with, fields
from flask_restful.reqparse import Argument
from .parsers import QueryChk


class SingleR(Resource):
    def __init__(self, arguments: List[Argument], fs: Optional[Dict[str, type]] = None, envelope: Optional[str] = None):
        self.parser = reqparse.RequestParser()
        for arg in arguments:
            self.parser.add_argument(arg)

        if fields:
            self.method_decorators = {'get': [marshal_with(fs, envelope)]}


class ListR(Resource):
    def __init__(self, query, arguments: List[Argument] = None,
                 searchable=None, order=None, fs: Optional[Dict[str, type]] = None,
                 envelope: Optional[str] = None):

        self.query = query

        if arguments:
            self.parser = reqparse.RequestParser()
            for arg in arguments:
                self.parser.add_argument(arg)

        self.get_parser = reqparse.RequestParser()
        if searchable:
            self.get_parser.add_argument('q', required=False, type=QueryChk(searchable, self.query))

        if order:
            pass #TODO add order option

        if fields:
            self.method_decorators = {'get': [marshal_with(fs, envelope)]}
