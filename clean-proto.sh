#!/usr/bin/bash

# clean gRPC code from directory protos
rm -rf protos

# update directories if needed
directories="app_service database influxdb logic mqtt user_api"

for dir in $directories; do
    rm -rf "$dir/app/protos"
done
