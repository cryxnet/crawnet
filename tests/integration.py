import requests
import time

def test_reach_website():
    website_url = "http://127.0.0.1:3000"

    print("[~] Test if we can reach the website")
    response = requests.get(website_url)
    assert response.status_code == 200, "Unable to reach website"
    print("[+] Success")

def test_reach_api():
    api_url = "http://127.0.0.1:5000"

    print("[~] Test if we can reach the API")
    response = requests.get(api_url)
    assert response.status_code == 200 or response.status_code == 404, "Unable to reach API"
    print("[+] Success")

def test_reach_neo4j():
    neo4j_url = "bolt://127.0.0.1:7687"

    print("[~] Test if we can connect to Neo4j")
    from neo4j import GraphDatabase
    try:
        driver = GraphDatabase.driver(neo4j_url, auth=("neo4j", "neo4j123"))
        with driver.session() as session:
            session.run("MATCH (n) RETURN n LIMIT 1")
    except Exception as e:
        assert False, f"Unable to connect to Neo4j: {e}"
    finally:
        driver.close()
    print("[+] Success")

def test_api_website_communication():
    website_url = "http://127.0.0.1:3000/graph"

    print("[~] Test if we can reach the API from the website")
    response = requests.get(website_url)
    assert response.status_code == 200, "Unable to reach API from website"
    print("[+] Success")

def test_api_neo4j_communication():
    api_url = "http://127.0.0.1:5000/domain"

    print("[~] Test if the API works with Neo4j")
    response = requests.get(api_url)
    assert response.json() == {'nodes': [], 'relationships': []}, "Unable to retrieve data from Neo4j via API"
    print("[+] Success")

# Run the tests
if __name__ == "__main__":
    print("[~] Started the tests...")
    test_reach_website()
    test_reach_api()
    test_reach_neo4j()
    test_api_website_communication()
    test_api_neo4j_communication()
