from app.server.werzeug import url_map
from sqlalchemy.ext.declarative import declared_attr

from app.utils.route import route


class Route:
    __url_prefix__ = "/"

    def __init__(self):
        self.url_map = url_map
        self.register_crud()

    def register_crud(self):
        @route(f"{self.__url_prefix__}/create", methods=["POST"])
        def create(self):
            return "<html>OK<html>"

        @route(f"{self.__url_prefix__}/get", methods=["GET"])
        def get(self):
            return "<html>OK<html>"

        @route(f"{self.__url_prefix__}/update", methods=["PUT", "PATCH"])
        def update(self):
            return "<html>OK<html>"

        @route(f"{self.__url_prefix__}/delete", methods=["DELETE"])
        def delete(self):
            return "<html>OK<html>"
