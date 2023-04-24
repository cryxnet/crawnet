from models.core import Model

class Registrar(Model):
    def __init__(self, name: str):
        self.name = name
