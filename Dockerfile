FROM python:3.11-slim

RUN apt-get update
RUN apt-get install -y git

WORKDIR /ipget

COPY .git .git
COPY ipget ipget
COPY requirements.txt .
ADD https://git.io/GeoLite2-City.mmdb resources/GeoLite2-City.mmdb

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV GEOIP false
ENV REVERSE_DNS_LOOKUP false

CMD ["gunicorn", "-c", "ipget/gunicorn.py", "ipget.ipget:app"]
