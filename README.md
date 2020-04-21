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

## ADD YOUR OWN ANALYSIS

In order to add your analysis you can use the template we provided.
The `service_template` folder contains the code necessary to start building your microservice.

- First of all you can develop your analysis algortim in `service_template.py`.
- Then you should setup the webserver, in particular:
	- you must set custom port where webserver is listening.
	- you must customize the API structure in `swagger.yml` in order to fit to your needs.
- To finalize you need to rename properly folder and files.