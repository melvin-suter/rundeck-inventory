#!/bin/sh

cd /app
mkdir -p $(dirname $OUTPUT_PATH)
crond -f