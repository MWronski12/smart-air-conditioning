#!/usr/bin/bash

mkdir -p protos

# generate gRPC code from directory protos into directory protos
source venv/bin/activate
python3 -m grpc_tools.protoc -Iapp/protos=./protobufs --python_out=protos --grpc_python_out=protos --pyi_out=protos protobufs/*.proto

# update directories if needed
directories="app_service database influxdb logic mqtt"

for dir in $directories; do
    mkdir -p "$dir/app/protos"
    cp -r protos/* "$dir/"
    touch "$dir/app/protos/__init__.py"
done
