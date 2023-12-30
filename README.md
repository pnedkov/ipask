# IP Get
Another ifconfig-like web application. This one is written in Python with Flask framework.

---
## Getting started

Install Python:
```
pacman -S python
```

Clone the git repository:
```sh
git clone https://github.com/pnedkov/ipget.git
cd ipget/
```

Create and activate the Python virtual environment:
```sh
python -m venv .venv
source .venv/bin/activate
```

Install the required Python packages:
```sh
pip install -r requirements.txt
```

---
## Run from the git repository:
```sh
./run.sh
```
Environment variables:
| ENV var | Default value |
| :----: | :----: |
| GUNICORN_SERVER | ipget |
| [GUNICORN_BIND](https://docs.gunicorn.org/en/stable/settings.html#bind) | "0.0.0.0:8080" |
| [GUNICORN_WORKERS](https://docs.gunicorn.org/en/stable/settings.html#workers) | CPU Cores * 2 + 1 |
| [GUNICORN_THREADS](https://docs.gunicorn.org/en/stable/settings.html#threads) | 1 |

Overwriting the default values (optional):
```sh
GUNICORN_WORKERS=4 GUNICORN_THREADS=2 ./run.sh
```

To run `ipget` without the WSGI server (gunicorn):
```sh
python run.py
```

Test:
```sh
$ curl <host>:8080[/ip|/ua|/headers]
$ wget -qO - <host>:8080[/ip|/ua|/headers]
```
Or navigate to `http://<host>:8080` from your browser.

---
## Run as a stand-alone container

Install and start Docker:
```sh
sudo pacman -S docker docker-compose docker-buildx
sudo usermod -aG docker $USER
sudo systemctl enable -now docker.service
```

Build the container:
```sh
docker build -t ipget .
```

Run:
```sh
docker run --rm -p 8080:8080 ipget
```

Test:
```sh
curl <host>:8080[/ip|/ua|/headers]
wget -qO - <host>:8080[/ip|/ua|/headers]
```
Or navigate to `http://<host>:8080` from your browser.

---
## Run with Docker Compose behind nginx reverse proxy

Generate the test key and certificate utilized by the nginx reverse proxy.

Review the environment variables inside `resources/generate_cert.sh` and change them accordingly before you run the script.
```sh
CN=yourdomain.com DAYS=365 ./resources/generate_cert.sh
```
Or you could use your own key and certificate. `docker-compose.yaml` expects to find them here:
- $HOME/.nginx/key.pem
- $HOME/.nginx/cert.pem

Run:
```sh
docker compose up -d
```
This will pull the latest `ipget` container from https://hub.docker.com.

Test:
```sh
curl -kL <host>[/ip|/ua|/headers]
wget --no-check-certificate -qO - <host>[/ip|/ua|/headers]
```
Or navigate to `<host>` from your browser. It will automatically redirect to https and you have to accept the self-signed certificate.
