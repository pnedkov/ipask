FROM python:3.11-slim

WORKDIR /ipget

COPY ipget/ /ipget
COPY requirements.txt /ipget

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV IP_API false

CMD ["gunicorn", "-c", "gunicorn.py", "ipget:app"]
