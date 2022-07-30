#!/usr/bin/env bash

echo "Launching hammer in a container"
docker run --rm -it -v $PWD/results:/app/results --network flash_hammer-net frenchben/ramp:1
