from neo4j import GraphDatabase

class Database:
    
    def __init__(self, uri, user, pwd):
        self.uri = uri
        self.user = user
        self.pwd = pwd
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.pwd))
        except Exception as e:
            print("Failed to create the driver: ", e)
        
    def close(self):
        self.driver.close()
        
    def query(self, query, parameters=None, db=None):
        response = None
        try: 
            response = list(self.driver.session().run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if self.driver.session() is not None:
                self.driver.session().close()
        return response
