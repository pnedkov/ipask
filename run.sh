#!/bin/sh

gunicorn -c ipask/gunicorn.py ipask.ipask:app
