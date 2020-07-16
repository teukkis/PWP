import json
from flask import Response, request, url_for
from foodManager.constants import *
from foodManager.models import *
from foodManager.utils.masonbuilder import MasonBuilder

class ResponseBuilder(MasonBuilder):

    def add_control(self):
        self.add_control(
            "",
            url_for(),
            method="",
            title="",
            encoding="json",
            schema=""
        )

