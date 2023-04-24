import os
from flask import Flask, request, jsonify
from services.intelligence import IntelligenceService
from services.neo4j import Neo4jService
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask("CRAWNET")
engine = Neo4jService(os.environ.get("NEO4J_CONNECTION_URI"), (os.environ.get("NEO4J_USERNAME"), os.environ.get("NEO4J_PASSWORD")))
intelligence = IntelligenceService()
cors = CORS(app)

@app.route('/domain/<domain>', methods=['POST'])
def discover_domain_route(domain):
    result = intelligence.collect(engine, domain)
    return "DONE!"

@app.route('/domain/<name>', methods=['get'])
def get_domain_nodes(name):
    result = engine.get_domain_related_nodes(name)
    return result


@app.route('/domain', methods=['get'])
def get_all_nodes():
    result = engine.get_all_nodes()
    return jsonify(result)

if __name__ == "__main__":
  app.run()
