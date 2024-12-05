from neo4j import GraphDatabase
import requests
from requests.auth import HTTPBasicAuth
import re 
import os


def get_repos_from_quotas(url, token):
    art_header = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=art_header)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")


class Graph:

    def __init__(self, uri):
        self.driver = GraphDatabase.driver(uri)        

    def close(self):
        self.driver.close()

    def create_graph(self):
        with self.driver.session() as session:
            session.execute_write(self._create_graph)
    
    def clear_graph(self):
        with self.driver.session() as session:
            session.execute_write(self._clear_graph)
    
    @staticmethod
    def _clear_graph(tx):
        tx.run("""
               MATCH (n)
               DETACH DELETE n;
            """)

    def insert_repos(self, repos_data):
            with self.driver.session() as session:
                for repo in repos_data:
                    session.execute_write(self._create_repo, repo)

            with self.driver.session() as session:
                for repo in repos_data:
                    for member_repo in repo.get("repositories", []):
                        if not self._is_url(member_repo):
                            repo_name = repo["key"]
                            session.execute_write(self._create_membership_relation, repo_name, member_repo)


    @staticmethod
    def _is_url(text):
        url_pattern = re.compile(r'https?://')
        return url_pattern.match(text) is not None
    
    @staticmethod
    def _create_repo(tx, repo):
        label = repo["type"]
        query = f"""
        MERGE (r:{label} {{name: $name}})
        SET r.packageType = $packageType,
            r.dockerPort = $dockerPort,
            r.owners = $owners
        """
        tx.run(query, name=repo["key"],
                      packageType=repo["packageType"],
                      dockerPort=repo["description"],
                      owners=repo["notes"])
        
    @staticmethod
    def _create_membership_relation(tx, repo_name, member_repo_name):
        query = """
        MATCH (r {name: $repo_name})
        MATCH (m {name: $member_repo_name})
        MERGE (r)-[:MEMBER_OF]->(m)
        """
        tx.run(query, repo_name=repo_name, member_repo_name=member_repo_name)

if __name__ == "__main__":

    uri_neo = os.getenv("NEO4J_URI")
    url = os.getenv("ART_URI")
    token=os.getenv("ART_TOKEN")
    repos_data = get_repos_from_quotas(url, token)
    result = []
    for type, repos in repos_data.items():
        for repo in repos:
            repo_with_type = {'type': type, **repo}
            result.append(repo_with_type)

    app = Graph(uri_neo)
    app.clear_graph()
    app.insert_repos(result)
    app.close()

    