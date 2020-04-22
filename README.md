# repository_analysis
Extensible framework to perform analysis over GitHub users and repositories.


## LOCALHOST
In order to run locally these analysis tools, you must to start the servers who are responsible to catch requests from GUI ( frontend ) and then start the GUI's server.

How to start services:

>`$ cd ./SERVICE-YOU-NEED`

>`$ python3 server.py`

How to start GUI:
> `$cd ./frontend`

> `$python3 server.py`

GUI is working on localhost:5000, services are listening on following ports (5001 to 5003).

## DOCKER SERVICES
If you want use our microservices using the powerful Docker Swarm infrastructure you should follow the complete guideline to create:

- Docker shared volume `my-volume`.
- Docker `images` of services.

Then you are able to launch our microservices as `docker services` enjoying benefits as automatic `replication` and automatic `load-balancing`.

### BUILD DOCKER IMAGES
NOTE: we are building these images from our custom ubuntu image `ubuntu-base.tar.gz`.

```bash
$ docker build -t hotspot -f hotspot/Dockerfile .
$ docker build -t change-coupling -f change_coupling/Dockerfile .
$ docker build -t skill-analysis -f skill_analysis/Dockerfile .
...
$ docker build -t frontend -f frontend/Dockerfile .
```

### CREATE DOCKER SERVICES

```bash
$ docker service create \
  --replicas=4 \
  --name hotspot-service \
  --mount source=my-volume,target=/home/utils \
  hotspot
$ docker service create \
  --replicas=4 \
  --name change-coupling-service \
  --mount source=my-volume,target=/home/utils \
  change-coupling
$ docker service create \
  --replicas=4 \
  --name skill-analysis-service \
  --mount source=my-volume,target=/home/utils \
  skill-analysis
...
$ docker service create \
  --replicas=4 \
  --name frontend-service \
  --mount source=my-volume,target=/home/utils,readonly \
  frontend

```


## ADD YOUR OWN ANALYSIS

In order to add your analysis you can use the template we provided.
The `service_template` folder contains the code necessary to start building your microservice.

- First of all you can develop your analysis algortim in `service_template.py`.
- Then you should setup the webserver, in particular:
	- you must set custom port where webserver is listening.
	- you must customize the API structure in `swagger.yml` in order to fit to your needs.
- To finalize you need to rename properly folder and files.