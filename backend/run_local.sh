#!/usr/bin/bash

export DATA_PATH="$PWD/../data"
export MODELS_PATH="$PWD/../models"

uvicorn --host "0.0.0.0" --port 8501 main:app