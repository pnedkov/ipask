# IP Get
Another ifconfig-like web application. This one is written in Python with Flask framework.


## Clone the Git repository
```
git clone https://github.com/pnedkov/ipget.git
cd ipget/
```
---

## Generate the test key-pair
Review the environment variables inside `resources/generate_cert.sh` and change them accordingly before you run the script.
```
CN=yourdomain.com DAYS=365 ./resources/generate_cert.sh
```
Or you could use your own key-pair. `docker-compose.yaml` expects to find them here:
- $HOME/.nginx/key.pem
- $HOME/.nginx/cert.pem
---

## Run from the source
```
./run.sh
```
Environment variables:
| ENV var | Default value |
| :----: | :----: |
| GUNICORN_SERVER | ipget |
| [GUNICORN_BIND](https://docs.gunicorn.org/en/stable/settings.html#bind) | "0.0.0.0:5000" |
| [GUNICORN_WORKERS](https://docs.gunicorn.org/en/stable/settings.html#workers) | CPU Cores * 2 + 1 |
| [GUNICORN_THREADS](https://docs.gunicorn.org/en/stable/settings.html#threads) | 1 |

Overwriting the default values:
```
GUNICORN_BIND="127.0.0.1:8000" GUNICORN_WORKERS=4 GUNICORN_THREADS=2 ./run.sh
```

To run `ipget` without the WSGI server (gunicorn):
```
python run.py
```
---

## Prerequisites for running in a container
Install and start Docker
```
pacman -S pacman -S docker-compose docker-buildx
systemctl enable -now docker.service
```
---

## Build a Docker container
```
docker build -t ipget .
```
---

## Run with Docker Compose
Review and update `image:` and the `GUNICORN_*` environment variables in `docker-compose.yaml`.
```
docker compose up -d
```
---

## Test with a web browser and from a command line
```
$ curl http://10.100.0.52:5000
10.100.0.18
$ curl http://10.100.0.52:5000/ip
10.100.0.18
$ curl http://10.100.0.52:5000/ua
curl/8.0.1
$ wget -qO - http://10.100.0.52:5000
10.100.0.18
$ wget -qO - http://10.100.0.52:5000/ua
Wget/1.21.3
$
```
