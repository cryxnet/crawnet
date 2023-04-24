from models.core import Model

class Location(Model):
    def __init__(self, city: str, region: str, country: str):
        self.city = city
        self.region = region
        self.country = country
