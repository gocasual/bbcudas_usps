'''
Script to show how to connect to and query the graph with python. 
'''
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

def driver():
    URI = os.getenv("NEO4J_URI")
    USERNAME = os.getenv("NEO4J_USERNAME")
    PASSWORD = os.getenv("NEO4J_PASSWORD")
    AUTH = (USERNAME, PASSWORD)

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        
    query = '''
        MATCH (m:mailPiece)-[r:`goes to`] -> (o:destination) 
        WHERE o.destaddress_STATENAME = "Florida"
        RETURN m, r, o
        '''

    records = driver.execute_query(
        query,
        database_="neo4j"
    )

print(records)

driver.close()