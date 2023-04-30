from models.core import Model
from models.hosting import Hosting
from models.ipaddress import IPAddress
from models.registrar import Registrar
from models.location import Location

class Domain(Model):
    def __init__(self,
                 name,
                 ipaddress: IPAddress,
                 whois_records,
                 hosting_provider: Hosting,
                 registrar: Registrar,
                 certificate_fingerprint,
                 location: Location,
                 subdomains):

        self.name = name
        self.ipaddress = ipaddress
        self.whois_records = whois_records
        self.hosting_provider = hosting_provider
        self.registrar = registrar
        self.certificate_fingerprint = certificate_fingerprint
        self.location = location
        self.subdomains = subdomains
