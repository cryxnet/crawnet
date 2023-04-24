from models.core import Model
from models.location import Location

class IPAddress(Model):
    def __init__(self, address: str, location: Location):
        self.address = address
        self.location = location
