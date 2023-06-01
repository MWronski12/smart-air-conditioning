#!/usr/bin/bash

set -e

mkdir -p protos

source venv/Scripts/activate
pip install -r requirements.txt

# generate gRPC code from directory protobufs into directory protos
python -m grpc_tools.protoc -Iapp/protos=./protobufs --python_out=protos --grpc_python_out=protos --pyi_out=protos protobufs/*.proto

# update directories if needed
directories="database influxdb logic mqtt user_api"

for dir in $directories; do
    mkdir -p "$dir/app/protos"
    cp -r protos/* "$dir/"
    touch "$dir/app/protos/__init__.py"
done
