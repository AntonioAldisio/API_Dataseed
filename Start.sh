#!/bin/bash
echo "Irei esperar 15 segundos"
sleep 15

echo "Realizando migrations"
yoyo apply --all

if [ $? -eq 0 ]; then
    echo "Migrations realizada com sucesso"
    uvicorn main:app --reload --host 0.0.0.0 --port 80
else
    echo "Error: yoyo apply failed. Application startup aborted."
fi
