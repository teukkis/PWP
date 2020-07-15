import json
from flask import Response, request, url_for
from food_manager.constants import *
from food_manager.models import *

class ResponseBuilder(MasonBuilder):

    def add_control(self):
        self.add_control(
            "",
            url_for(),
            method:"",
            title="",
            encoding="json",
            schema=""
        )

