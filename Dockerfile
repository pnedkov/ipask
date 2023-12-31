FROM python:3.11-slim

WORKDIR /ipget

COPY ipget/ .
COPY requirements.txt .
ADD https://git.io/GeoLite2-City.mmdb resources/GeoLite2-City.mmdb

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV GEOIP true
ENV REVERSE_DNS_LOOKUP true

CMD ["gunicorn", "-c", "gunicorn.py", "ipget:app"]
