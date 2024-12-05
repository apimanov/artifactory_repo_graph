# Artifactory repository linkage

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Screenshot](#screenshot)

## About <a name = "about"></a>

Script draws graph artifactory repositories with their connections including descriptions

## Getting Started <a name = "getting_started"></a>

The script uses the neo4j vector database to upload and draw links. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Installing

Edit docker-compose.yml file by specifying the uri and token artifactory instance


```
- ART_URI=https://ArtifactoryHost/api/repositories/configurations
- ART_TOKENT=ADMIN TOKEN HERE
```

run docker compose file

```
sudo docker-compose up --build
```

Go to the browser to open WEBUI <a name = "localhost:7474">http://localhost:7474/browser/</a>

## Usage <a name = "usage"></a>

Example of Cypher requests:

It will show what connections the repository SOME-REPO-NAME has:
```
MATCH path = (root {name: "SOME-REPO-NAME"})-[:MEMBER_OF*]->(connected)
RETURN path

MATCH path = (root {name: "SOME-REPO-NAME"})-[:MEMBER_OF*]->(connected)
WHERE NOT connected:REMOTE
RETURN path
```
