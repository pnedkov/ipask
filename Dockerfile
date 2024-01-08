FROM python:3.11-slim

RUN apt-get update
RUN apt-get install -y git

WORKDIR /ipask

RUN git clone https://github.com/pnedkov/ipask.git .
RUN pip install --no-cache-dir -r requirements.txt

ADD https://git.io/GeoLite2-City.mmdb resources/GeoLite2-City.mmdb

EXPOSE 8080

ENV IPASK_PROD true
ENV GEOIP false
ENV REVERSE_DNS_LOOKUP false

CMD ["gunicorn", "-c", "ipask/gunicorn.py", "ipask.ipask:app"]
