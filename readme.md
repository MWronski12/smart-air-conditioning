# Microservices

This repository contains code for the microservices.
To run the microservices, you need to have docker installed.

## Setting up the environment

First, you have to create a new python virtual environment:
```bash
python3 -m venv venv
```
Then you have to generate protobuf files using the `generate-proto.sh` script:
```bash
chmod +x generate-proto.sh
./generate-proto.sh
```
This script will activate the virtual environment and install the required dependencies.
Then it will generate the python files into `proto` directory based on `.proto` files located in `protobufs` directory.
It will also copy the generated files into each microservice directory.


### InfluxDB configuration
To user InfluxDB, you have to create a `.env` file in the root directory of the project.
This file should contain the following variables:
```bash
INFLUXDB_HOST=<influxdb_host>
INFLUXDB_TOKEN=<influxdb_password>
INFLUXDB_ORG=<influxdb_org>
INFLUXDB_BUCKET=<influxdb_bucket>
```

## Running the microservices

To run the microservices using docker-compose, you can use `docker-compose.yml` file:
```bash
docker-compose up --build
```

## Cleaning up the generated files

To clean the generated files, you can use the `clean-proto.sh` script:
```bash
chmod +x clean-proto.sh
./clean-proto.sh
```
