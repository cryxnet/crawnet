from services.neo4j import Neo4jService
from services.client import Client
from models import Domain, Registrar, Location, Hosting, Nameserver, IPAddress
import socket
import whois
import requests
import re
import json

class IntelligenceService():
    def __init__(self):
        self.sources = {"ipinfo": "https://ipapi.co/IPADDRESS/json/", "crtsh": "https://crt.sh/?q=DOMAIN&output=json"}
        self.client = Client(headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"})

    # TODO: implement __getIPAddressFromDomain
    def __getIPAddressFromDomain(self, domain: str):
        """
        This method gets the IP address from a domain.
        """
        try: ip = socket.gethostbyname(domain)
        except: ip = "unknow"

        location = self.__getLocationFromIP(ip)

        return IPAddress(address=ip, location=location)

    # TODO: implement __getDNSRecordsFromDomain
    def __getDNSRecordsFromDomain(self, domain: str):
        """
        This method gets the DNS records from a domain.
        """
        return "NOT IMPLEMENT"

    def __getWHOISFromDomain(self, domain: str):
        """
        This method gets the WHOIS from a domain.
        """
        try: whois_data = whois.whois(domain).text
        except: whois_data = "unknow"

        return whois_data

    def __getHostingProviderFromIP(self, ipaddress: str):
        """
        This method gets the hosting provider from a ipaddress.
        """
        try: response = self.client.get(self.sources['ipinfo'].replace('IPADDRESS', ipaddress)); org = response.json().get('org')
        except: response = "unknow"; org = "unknow"

        location = self.__getLocationFromIP(ipaddress)

        ipaddress = IPAddress(address=ipaddress, location=location)

        hosting_provider = Hosting(organization=org, ipaddress=ipaddress)

        return hosting_provider

    def __getThreatStatusFromDomain(self, domain: str):
        """
        This method gets information about threats from a domain.
        """
        return "raise NotImplementedError()"

    def __getSubdomainFromDomain(self, domain: str):
            subdomains = []

            # Technique 1: Extract subdomains from Certificate Transparency logs
            try:
                certificates = self.__getCertificateFingerprintFromDomain(domain)
                for certificate in certificates:
                    subdomains.append(certificate['name_value'])
            except Exception as e:
                print(f"Error extracting subdomains from Certificate Transparency logs: {e}")

            # Technique 2: Google dorking
            try:
                response = self.client.get(f'https://www.google.com/search?q=site:{domain}&start=0')
                urls = re.findall(r'<a href="([^"]+)"', response.text)
                for url in urls:
                    match = re.search(r'https?://([\w\.-]+)\.{}.*'.format(domain), url)
                    if match:
                        subdomains.append(match.group(1))
            except Exception as e:
                print(f"Error performing Google dorking: {e}")

            return subdomains

    def __getRegistrarFromDomain(self, domain: str):
        """
        This method gets the registrar information of a domain.
        """
        # Perform a WHOIS lookup using the python-whois library
        try: w = whois.whois(domain)
        except: w = "unknow"

        if not w == "unknow":
            return Registrar(name=w.registrar) if w.registrar is not None else 'unknown'

        return "unknow"

    def __getCertificateFingerprintFromDomain(self, domain: str):
        """
        This method gets certificates fingerprints from a domain.
        """
        try: response = self.client.get('https://crt.sh/?q=DOMAIN&output=json'.replace('DOMAIN', domain)); fingerprints = response.json()
        except: fingerprints = "unknow"

        return fingerprints

    def __getLocationFromIP(self, ipaddress: str):
        """
        This method gets location information from ip address
        """
        try: response = self.client.get(self.sources['ipinfo'].replace('IPADDRESS', ipaddress)); response = response.json(); location = Location(city=response["city"], region=response["region"], country=response["country"])
        except: location = "unknow"

        return location

    # TODO: implement this (updated with params etc)
    def __collect_domain(self, domain: str):
        """
        This method collects all information of a domain and its subdomains recursively.
        """

        print("[~] Starting collecting data with different techniques")

        ipaddress = self.__getIPAddressFromDomain(domain)
        dns_records = self.__getDNSRecordsFromDomain(domain)
        whois_records = self.__getWHOISFromDomain(domain)
        hosting_provider = self.__getHostingProviderFromIP(ipaddress.address)
        threat_status = self.__getThreatStatusFromDomain(domain)
        registrar = self.__getRegistrarFromDomain(domain)
        certificate_fingerprint = self.__getCertificateFingerprintFromDomain(domain)
        location = self.__getLocationFromIP(ipaddress.address)
        subdomains = self.__getSubdomainFromDomain(domain)

        domain_object = Domain(name=domain,
                                ipaddress=ipaddress,
                                dns_records=dns_records,
                                whois_records=whois_records,
                                hosting_provider=hosting_provider,
                                threat_status=threat_status,
                                registrar=registrar,
                                certificate_fingerprint=certificate_fingerprint,
                                location=location,
                                subdomains=subdomains)

        subdomains_count = len(domain_object.subdomains)

        return domain_object

    def remove_duplicates(self, lst, custom_element=None):
        """
        Removes duplicates from a list and a custom-named element (if provided).
        Returns the modified list.
        """
        result = []
        seen = set()
        for item in lst:
            if item != custom_element and item not in seen:
                seen.add(item)
                result.append(item)
        return result

    def add_domain_nodes():
        pass

    def collect(self, engine: Neo4jService, domain: str):
        # Get model objects
        parent_domain_object = self.__collect_domain(domain)
        domain_ipaddress_object = parent_domain_object.ipaddress
        domain_ipaddress_location_object = domain_ipaddress_object.location
        domain_hosting_object = parent_domain_object.hosting_provider
        domain_hosting_ipaddress_object = domain_hosting_object.ipaddress
        domain_hosting_ipaddress_location_object = domain_hosting_object.ipaddress.location
        domain_registrar_object = parent_domain_object.registrar
        domain_location_object = parent_domain_object.location

        # Creation of nodes and relationships
        if isinstance(domain_hosting_ipaddress_location_object, Location):
            domain_hosting_ipaddress_location_node_id = engine.add_location_node(domain_hosting_ipaddress_location_object)

        if isinstance(domain_registrar_object, Registrar):
            domain_registrar_node_id = engine.add_registrar_node(domain_registrar_object)

        if isinstance(domain_ipaddress_location_object, Location):
            domain_ipaddress_location_node_id = engine.add_location_node(domain_ipaddress_location_object)

        if isinstance(domain_ipaddress_object, IPAddress):
            domain_ipaddress_node_id = engine.add_ipaddress_node(domain_ipaddress_object)
            engine.pair_ipaddress_node(domain_ipaddress_node_id, domain_ipaddress_object)

        if isinstance(domain_hosting_ipaddress_object, IPAddress):
            domain_hosting_ipaddress_node_id = engine.add_ipaddress_node(domain_hosting_ipaddress_object)
            engine.pair_ipaddress_node(domain_hosting_ipaddress_node_id, domain_hosting_ipaddress_object)

        if isinstance(domain_hosting_object, Hosting):
            if domain_hosting_object.organization:
                domain_hosting_node_id = engine.add_hosting_node(domain_hosting_object)
                engine.pair_hosting_node(domain_hosting_node_id, domain_hosting_object)

        parent_domain_node_id = engine.add_domain_node(parent_domain_object)
        engine.pair_domain_node(parent_domain_node_id, parent_domain_object)

        # Collect subdomains
        subdomains = self.remove_duplicates(parent_domain_object.subdomains, custom_element=domain)
        subdomain_count = len(subdomains)

        for i in range(subdomain_count):
            subdomain = subdomains[i]

            print(f"[{i+1}/{subdomain_count}] Collecting information of subdomain: {subdomain}")

            # Collect subdomain entities
            subdomain_object = self.__collect_domain(subdomain)
            subdomain_ipaddress_object = subdomain_object.ipaddress
            subdomain_ipaddress_location_object = subdomain_ipaddress_object.location
            subdomain_hosting_object = subdomain_object.hosting_provider
            subdomain_hosting_ipaddress_object = subdomain_hosting_object.ipaddress
            subdomain_hosting_ipaddress_location_object = subdomain_hosting_object.ipaddress.location
            subdomain_registrar_object = subdomain_object.registrar
            subdomain_location_object = subdomain_object.location

            # Add domain entities
            if isinstance(subdomain_ipaddress_location_object, Location):
                subdomain_ipaddress_location_node_id = engine.add_location_node(subdomain_ipaddress_location_object)

            if isinstance(subdomain_hosting_ipaddress_location_object, Location):
                subdomain_hosting_ipaddress_location_node_id = engine.add_location_node(subdomain_hosting_ipaddress_location_object)

            if isinstance(subdomain_registrar_object, Registrar):
                subdomain_registrar_node_id = engine.add_registrar_node(subdomain_registrar_object)

            if isinstance(subdomain_ipaddress_object, IPAddress):
                subdomain_ipaddress_node_id = engine.add_ipaddress_node(subdomain_ipaddress_object)
                engine.pair_ipaddress_node(subdomain_ipaddress_node_id, subdomain_ipaddress_object)

            if isinstance(subdomain_hosting_ipaddress_object, IPAddress):
                subdomain_hosting_ipaddress_node_id = engine.add_ipaddress_node(subdomain_hosting_ipaddress_object)
                engine.pair_ipaddress_node(subdomain_hosting_ipaddress_node_id, subdomain_hosting_ipaddress_object)

            if isinstance(subdomain_hosting_object, Hosting):
                if subdomain_hosting_object.organization:
                    subdomain_hosting_node_id = engine.add_hosting_node(subdomain_hosting_object)
                    engine.pair_hosting_node(subdomain_hosting_node_id, subdomain_hosting_object)

            subdomain_node_id = engine.add_domain_node(subdomain_object)
            engine.pair_domain_node(subdomain_node_id, subdomain_object)

            engine.connect_to(parent_domain_node_id, "Domain", {"name": subdomain_object.name}, "RELATED_TO")
