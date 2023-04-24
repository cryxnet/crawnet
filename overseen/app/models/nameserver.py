from models.core import Model
from models.ipaddress import IPAddress

class Nameserver(Model):
    def __init__(self, address, ipaddress: IPAddress):
        self.address = address
        self.ipaddress = ipaddress
