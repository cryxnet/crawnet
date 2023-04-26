import requests
import time

class IntegrationTestCases:
    def test_reach_website(self):
        website_url = "http://localhost:3000"

        print("[~] Test if we can reach the website")
        response = requests.get(website_url)
        assert response.status_code == 200, "Unable to reach website"
        print("[+] Success")

    def test_reach_api(self):
        api_url = "http://localhost:5000"

        print("[~] Test if we can reach the API")
        response = requests.get(api_url)
        assert response.status_code == 200 or response.status_code == 404, "Unable to reach API"
        print("[+] Success")

    def test_reach_neo4j(self):
        neo4j_url = "bolt://localhost:7687"

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

    def test_api_website_communication(self):
        website_url = "http://localhost:3000/graph"

        print("[~] Test if we can reach the API from the website")
        response = requests.get(website_url)
        assert response.status_code == 200, "Unable to reach API from website"
        print("[+] Success")

    def test_api_neo4j_communication(self):
        api_url = "http://localhost:5000/domain"

        print("[~] Test if the API works with Neo4j")
        response = requests.get(api_url)
        assert response.json() == {'nodes': [], 'relationships': []} or response.status_code == 200, "Unable to retrieve data from Neo4j via API"
        print("[+] Success")

if __name__ == "__main__":
    print("[~] Starting the tests...")

    testcases = IntegrationTestCases()

    testcases.test_reach_website()
    testcases.test_reach_api()
    testcases.test_reach_neo4j()
    testcases.test_api_website_communication()
    testcases.test_api_neo4j_communication()
