# Panda Backend Developer Test

Panda Backend Developer Test

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Prerequisites

```
Docker 17.05+
Docker Compose 1.17+
```
# Solution Description

By looking at the nature of the csv data, it looks like list of **Transactions**.

## Building & Running Stack

```
docker compose -f local.yml build
docker compose -f local.yml up
```

## Browsable API Links

#### Upload CSV

http://localhost:8000/api/uploads/

#### Monitory Ingestion Process ( Flower )

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




