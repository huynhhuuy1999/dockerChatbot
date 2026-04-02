# actions/neo4j_client.py
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from typing import Optional, Dict

load_dotenv()  # load .env

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        if not (NEO4J_URI and NEO4J_USER and NEO4J_PASSWORD):
            raise RuntimeError("Neo4j credentials not set in environment variables")
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        session = _driver.session(database=NEO4J_DATABASE)
        _driver.verify_connectivity()

    return  _driver

def close_driver():
    global _driver
    if _driver:
        _driver.close()
        _driver = None