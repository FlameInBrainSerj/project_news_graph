#!/bin/bash

cd src

if [[ "${1}" == "celery" ]]; then
  celery --app=models_functionality.inference:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=models_functionality.inference:celery flower
 fi
