from models.core import Model
from models.ipaddress import IPAddress

class Hosting(Model):
    def __init__(self, organization: str, ipaddress: IPAddress):
        self.organization = organization
        self.ipaddress = ipaddress
