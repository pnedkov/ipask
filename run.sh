#!/bin/sh

gunicorn -c ipget/gunicorn.py ipget.ipget:app
