from app.database.base import Engine
from app.database.model import Model


class User(Model):
    def __init__(self):
        self.metadata.create_all(Engine)
        super().__init__()

    def test(self):
        pass
