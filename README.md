# Dynatrace - ApplicationOverviewDashboardGenerator

This script will create a new Application Overview Dashboard, with multiple tiles for every Application monitored.

![Dashboard example](img/Dashboard.PNG?raw=true "Dashboard example")


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This is a python script, so you will need [python installed](https://www.python.org/downloads/) to execute the script

URL from your Dynatrace environment

Dynatrace API Token

Dashboard template - provided in this repo [template.json](template.json) (the tiles will be replicated in the new dahsboard) 

Application tag applied to the elements: Application, Hosts, Services and Databases


### Generate Dynatrace API token

To create a new dashboard, the script use the Dynatrace Configuration API and Environment API. 
To create a new token, access to Dynatrace UI Settings > Integration > Dynatrace API > Generate token
The token will need the following rights:

```
Access problem and event feed, metrics and topology

Write configuration
```
![Generate token](img/Token.png?raw=true "Generate token")

## Edit script

Edit the dashboard.py file, include your Dynatrace cluster URL and API Token

```
ENV = 'https://YOUR-DYNATRACE-CLUSTER-URL'
TOKEN = 'YOUR-DYNATRACE-API-TOKEN'
```

## Running the tests

Execute the following command to run the script

```
py dashboard.py
```

The output will print the HTTP code, id of the new dashboards and URL
```
Response code: 201, Id new dashboards: 156ace3d-ea3f-471a-b723-219a15c46fb3, URL new dashboard: https://YOUR-DYNATRACE-CLUSTER-URL/#dashboard;id=156ace3d-ea3f-471a-b723-219a15c46fb3
```
