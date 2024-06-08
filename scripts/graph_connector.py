'''
Script to show how to connect to and query the graph with python. 

Use this as a python module and add:
from graph-connector import query_executor

To query data from neo4j simply write the query string and
pass that to the `query_executor` function. 
'''
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

def driver_connect(original_function):
    def driver_action(*args):
        URI = os.getenv("NEO4J_URI")
        USERNAME = os.getenv("NEO4J_USERNAME")
        PASSWORD = os.getenv("NEO4J_PASSWORD")
        AUTH = (USERNAME, PASSWORD)

        driver = GraphDatabase.driver(URI, auth=AUTH)
        driver.verify_connectivity()
        result = original_function(driver, *args)
        driver.close()
        return result
    return driver_action 


@driver_connect
def query_executor(driver, query):
    records = driver.execute_query(
        query,
        database_="neo4j"
    )
    return records


if __name__=='__main__':
    query = '''
        MATCH (m:mailPiece)-[r:`goes to`] -> (o:destination) 
        WHERE o.destaddress_STATENAME = "Florida"
        RETURN m, r, o
        '''
    data = query_executor(query)
    print(data)

