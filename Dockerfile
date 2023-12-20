FROM python:3.11-slim

WORKDIR /ipget

COPY ipget/ /ipget
COPY requirements.txt /ipget

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV WORKERS 2
ENV IP_API false
ENV FLASK_ENV production

ENTRYPOINT exec gunicorn -w $WORKERS -b 0.0.0.0:5000 ipget:app
