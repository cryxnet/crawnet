from base.service import Service
from neo4j import GraphDatabase
from models import Domain, Registrar, Location, Hosting, IPAddress
import os
import json
from typing import Dict

class Neo4jService(Service):
    def __init__(self, connection_uri, auth):
        self.driver = GraphDatabase.driver(connection_uri, auth=auth)
        self.session = self.driver.session()

    def connect_domains(self, node1_id: str, node2_id: str, relationship_name: str):
        """
        This method creates a relationship between two nodes by their id with a given relationship name
        """
        query = f"MATCH (a), (b) WHERE id(a) = $node1_id AND id(b) = $node2_id CREATE (a)-[:{relationship_name}]->(b)"
        self.session.run(query, node1_id=node1_id, node2_id=node2_id)

    def connect_to(self, node_id: int, target_label: str, target_requirements: Dict[str, str], relationship_type: str):
        """
        This method connects the current node to a node matching the target requirements using the given relationship type
        """
        query = (
            f"MATCH (a) WHERE ID(a) = {node_id}\n"
            f"MATCH (b:{target_label}) WHERE "
        )
        for key, value in target_requirements.items():
            query += f"b.{key} = '{value}' AND "
        query = query[:-5]
        query += f"\n"

        # Check if a relationship already exists
        query += f"MATCH (a)-[r:{relationship_type}]->(b)\n"
        query += f"WHERE ID(a) = {node_id} AND "
        for key, value in target_requirements.items():
            query += f"b.{key} = '{value}' AND "
        query = query[:-5]
        query += f"\n"

        query += "RETURN COUNT(r)"

        result = self.session.run(query)

        if result.single()[0] == 0:
            # Create the relationship if it does not exist
            query = (
                f"MATCH (a) WHERE ID(a) = {node_id}\n"
                f"MATCH (b:{target_label}) WHERE "
            )
            for key, value in target_requirements.items():
                query += f"b.{key} = '{value}' AND "
            query = query[:-5]
            query += f"\nCREATE (a)-[:{relationship_type}]->(b)"
            self.session.run(query)


    def add_location_node(self, location: Location):
        """
        This method adds a new location node to the database if it doesn't already exist.
        """

        does_exist = self.session.run("MATCH (n:Location {city: $city, country: $country, region: $region}) RETURN id(n) AS id", city=location.city, country=location.country, region=location.region)

        if does_exist.peek() is None:
            result = self.session.run(
                "MERGE (n:Location {city: $city, country: $country, region: $region}) RETURN id(n) AS id",
                city=location.city, country=location.country, region=location.region
            )

            return result.single()["id"]

        return does_exist.single()["id"]

    def add_ipaddress_node(self, ipaddress: IPAddress):
        """
        This method adds a new ipaddress node to the database if it doesn't already exist.
        """
        does_exist = self.session.run("MATCH (n:IPAddress {address: $address, location: $location}) RETURN id(n) AS id", address=ipaddress.address, location=json.dumps(ipaddress.location.get_data()) if not isinstance(ipaddress.location, str) else "unknown")

        if does_exist.peek() is None:
            result = self.session.run(
                "MERGE (n:IPAddress {address: $address, location: $location}) RETURN id(n) AS id",
                address=ipaddress.address, location=json.dumps(ipaddress.location.get_data()) if not isinstance(ipaddress.location, str) else "unknown"
            )
            return result.single()["id"]

        return does_exist.single()["id"]

    def add_hosting_node(self, hosting: Hosting):
        """
        This method adds a new hosting node to the database if it doesn't already exist.
        """
        does_exist = self.session.run("MATCH (n:Hosting {organization: $organization, ipaddress: $ipaddress}) RETURN id(n) AS id",  organization=hosting.organization, ipaddress=json.dumps(hosting.ipaddress.get_data()))

        if does_exist.peek() is None:
            result = self.session.run(
                "MERGE (n:Hosting {organization: $organization, ipaddress: $ipaddress}) RETURN id(n) AS id",
                organization=hosting.organization,
                ipaddress=json.dumps(hosting.ipaddress.get_data())
            )
            return result.single()["id"]

        return does_exist.single()["id"]

    def add_registrar_node(self, registrar: Registrar):
        """
        This method adds a new registrar node to the database if it doesn't already exist.
        """
        does_exist = self.session.run("MATCH (n:Registrar {name: $name}) RETURN id(n) AS id", name=registrar.name)

        if does_exist.peek() is None:
            result = self.session.run(
                "MERGE (n:Registrar {name: $name}) RETURN id(n) AS id",
                name=registrar.name
            )
            return result.single()["id"]

        return does_exist.single()["id"]

    def add_domain_node(self, domain: Domain) -> int:
        """
        This method adds a new domain node to the database if it doesn't already exist and returns its ID.
        """
        result = self.session.run("""MERGE (n:Domain{name: $name})
                          ON CREATE SET
                          n.ipaddress = $ipaddress,
                          n.dns_records = $dns_records,
                          n.whois_records = $whois_records,
                          n.hosting_provider = $hosting_provider,
                          n.threat_status = $threat_status,
                          n.registrar = $registrar,
                          n.certificate_fingerprint = $certificate_fingerprint,
                          n.location = $location
                          RETURN id(n) AS id""",
                          name=domain.name,
                          ipaddress=json.dumps(domain.ipaddress.get_data()) if not isinstance(domain.ipaddress, str) else "unknown",
                          dns_records=domain.dns_records,
                          whois_records=json.dumps(domain.whois_records),
                          hosting_provider=json.dumps(domain.hosting_provider.get_data()) if not isinstance(domain.hosting_provider, str) else "unknown",
                          threat_status=domain.threat_status,
                          registrar=json.dumps(domain.registrar.get_data()) if not isinstance(domain.registrar, str) else "unknown",
                          certificate_fingerprint=json.dumps(domain.certificate_fingerprint),
                          location=json.dumps(domain.location.get_data()) if not isinstance(domain.location, str) else "unknown")

        return result.single()["id"]

    def pair_domain_node(self, node_id: int, obj: Domain):
        # Connect domain to IP address
        self.connect_to(node_id, 'IPAddress', {'address': obj.ipaddress.address}, 'HOSTED_BY')
        # Connect domain to registrar
        if isinstance(obj.registrar, Registrar):
            self.connect_to(node_id, 'Registrar', {'name': obj.registrar.name}, 'REGISTERED_BY')

    def pair_hosting_node(self, node_id: int, node: Hosting):
        # Connect hosting provider to IP address
        self.connect_to(node_id, 'IPAddress', {'address': node.ipaddress.address}, 'HAS_IP_ADDRESS')

    def pair_ipaddress_node(self, node_id: int, node: IPAddress):
        # Connect IP address to location
        if isinstance(node.location, Location):
            self.connect_to(node_id, 'Location', {'city': node.location.city, 'region': node.location.region, 'country': node.location.country}, 'LOCATED_IN')

    def get_domain_related_nodes(self, domain_name: str):
        result = self.session.run(
                "MATCH (d:Domain {name: $domain_name})-[*]-(related)"
                "RETURN {node: d {.*, labels: labels(d)}, relationships: [r IN relationships(p) | {type: type(r), from: startNode(r).name, to: endNode(r).name, properties: r.*}]}, COLLECT({node: related {.*, labels: labels(related)}, relationships: [r IN relationships((d)-[*]-(related)) | {type: type(r), from: startNode(r).name, to: endNode(r).name, to_label: labels(endNode(r))[0], properties: r.*}]}) as related_nodes",
                domain_name=domain_name
            )

        records = result.single()
        return records

    def get_all_nodes(self):
        result = self.session.run(
          "MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN COLLECT(DISTINCT {id: ID(n), label: head(labels(n)), properties: properties(n)}) AS nodes, COLLECT(DISTINCT {from: ID(n), to: ID(m), type: type(r)}) AS relationships"
        )
        record = result.single()
        nodes = [dict(node) for node in record["nodes"]]
        relationships = [relationship_type for relationship_type in record["relationships"]]
        return {"nodes": nodes, "relationships": relationships}

# "MATCH (n)-[r]->(m) RETURN COLLECT(DISTINCT {id: ID(n), label: head(labels(n)), properties: properties(n)}) AS nodes, COLLECT(DISTINCT {from: ID(n), to: ID(m)}) AS relationships"
