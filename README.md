# Panda Backend Developer Test

Panda Backend Developer Test

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Prerequisites

```
Docker 17.05+
Docker Compose 1.17+
```
## Problem Description

* Design and build a scalable solution for processing very large data sets
* The system needs to process a CSV with a very large amount of data
* Ensure that the CSV data set is validated according to a given rule set
* System should be able to process data reliably and quickly

## Solution Description

1. Once a user uploads a CSV to the system, then the ingestion process begins.
   - Ingestion process: 
     * Make an API call to retrieve 2020 data on countries and exchange rates 
       against Euro from the bank API.
     * The API call is only performed once and the data is stored in a dict 
       so that we can look up the relevant exchange rate while processing the rows.
     * Data is then extracted from the CSV and is validated 
        against a given rule set. After the validation is successful, each 
        row is transformed by updating the currency to Euro.
     * The validated and processed data is then imported directly into the 
        database as CSV using psycopg2 copy_from function. 
     * The reason why the psycopg2 copy_from function was used over the normal
       tradition insert or copy command is for performance, as normal insert 
       statements have a lot of overhead.
     * The ingestion process runs on a separate Celery process. 

2. Limitations of the chosen solution:
     * The dict that stores the exchange rate data can use a large amount 
     of Memory as the date range grows beyond 5 years.

## Building & Running Stack

```
git clone git@github.com:matimuchauke/panda.git
cd panda
docker compose -f local.yml build
docker compose -f local.yml up
```

## Browsable API Links

#### Upload CSV

http://localhost:8000/api/uploads/

files under samples directory

#### Monitor Ingestion Process ( Flower )

http://localhost:5555/tasks

Username : XJjSeZLLdplipVKXHGuzmQSdcDtdYDod

Password : 6BlrMJdNe11PmSbiVwjUXDVh66ydLCQd6ERmx2xvm5rrJ6lLs8wL704dTrte62FN

##### All transactions

http://localhost:8000/api/transactions/

##### Country filtered transactions

http://localhost:8000/api/transactions/?country=US

##### Date filtered transactions

http://localhost:8000/api/transactions/?date=2020/07/11

##### Date & Country Filtered Transactions

http://localhost:8000/api/transactions/?country=US&date=2020/07/11
