#!/bin/bash
for container_id in $(docker ps --format "{{.ID}}")
do
    docker kill $container_id
done
