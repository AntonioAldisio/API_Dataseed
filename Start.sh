#!/bin/bash

sleep 15

yoyo apply --all

if [ $? -eq 0 ]; then
    uvicorn main:app --reload --host 0.0.0.0 --port 80
else
    echo "Error: yoyo apply failed. Application startup aborted."
fi
