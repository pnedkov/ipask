#!/bin/sh

gunicorn -w ${WORKERS:-2} -b 0.0.0.0:5000 ipget.ipget:app
