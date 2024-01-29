# IP Ask

`whatsmyip` type of web application written in Python with Flask framework

[ipask.me](https://ipask.me)

---

<details>
<summary>

## TL;DR

</summary>

- Run as a stand-alone container

  ```sh
  docker run -d -p 8080:8080 prestigen/ipask
  ```

- Run with nginx reverse proxy

  ```sh
  git clone https://github.com/pnedkov/ipask.git
  cd ipask/
  CN=yordomain.com ./resources/generate_cert.sh
  docker compose -f compose.yaml up -d
  ```

</details>

---

<details>
<summary>
  
## Usage

</summary>

- If `ipask` is running as a stand-alone application on the default port `8080`:

  ```sh
  $ curl <host>:8080
  $ wget -qO - <host>:8080
  ```

  Or navigate to `http://<host>:8080` from your browser.

- If `ipask` is running with nginx reverse proxy:

  ```sh
  $ curl -kL <host>
  $ wget --no-check-certificate -qO - <host>
  ```

  Or navigate to `<host>` from your browser. It will automatically redirect to https.

- Available URL paths:
  | Path | Alias | Description |
  | --- | --- | --- |
  | `/ip` | | IP address |
  | `/host` | `/h` | Hostname or FQDN (if `REVERSE_DNS_LOOKUP` is enabled) |
  | `/xff` | | X-Forwarded-For header |
  | `/city` | `/ci` | City (if `GEOIP` is enabled) |
  | `/region` | `/reg` | Region (if `GEOIP` is enabled) |
  | `/country` | `/co` | Country (if `GEOIP` is enabled) |
  | `/location` | `/loc` | GPS Coordinates (if `GEOIP` is enabled) |
  | `/ua` | | User-Agent request header |
  | `/headers` | `/he` | All headers |
  | `/version` | `/ver` | Application version (commit hash) |

</details>

---

<details>
<summary>

## Run from the source code

</summary>

### Prerequisites

- Install Git and Python:

  ```
  sudo pacman -S git python
  ```

- Clone the git repository:

  ```sh
  git clone https://github.com/pnedkov/ipask.git
  cd ipask/
  ```

- Create and activate the Python virtual environment:

  ```sh
  python -m venv .venv
  source .venv/bin/activate
  ```

- Install the required Python packages:

  ```sh
  pip install -r requirements.txt
  ```

- (Optional) Download the GeoIP database:

  The GeoIP feature is toggled with the `GEOIP` environment variable which is disabled by default. Enabling `GEOIP` would not do any good if the client's IP address is from a private network. The `GeoLite2-City.mmdb` file is being included in the container - check the `Dockerfile`.

  Credit: https://github.com/P3TERX/GeoLite.mmdb

  - wget:
    ```
    wget git.io/GeoLite2-City.mmdb -P resources/
    ```
  - curl:
    ```
    curl -L git.io/GeoLite2-City.mmdb -o resources/GeoLite2-City.mmdb
    ```

- Environment variables:
  | Environment variable | Default value |
  | --- | --- |
  | GEOIP | `false` |
  | REVERSE_DNS_LOOKUP | `false` |

### Run

- Run using `run.py`:

  ```sh
  python run.py
  ```

  Example:

  ```sh
  REVERSE_DNS_LOOKUP=true python run.py
  ```

- Run using `run.sh` (recommended):

  This will run the application with the Python WSGI HTTP Server - [gunicorn](https://gunicorn.org):

  ```sh
  ./run.sh
  ```

  Gunicorn-specific environment variables:
  | Environment variable | Default value |
  | --- | --- |
  | GUNICORN_SERVER | `ipask` |
  | [GUNICORN_WORKERS](https://docs.gunicorn.org/en/stable/settings.html#workers) | `CPU Cores * 2 + 1` |
  | [GUNICORN_THREADS](https://docs.gunicorn.org/en/stable/settings.html#threads) | `1` |

  Example:

  ```sh
  REVERSE_DNS_LOOKUP=true GUNICORN_WORKERS=3 ./run.sh
  ```

</details>

---

<details>
<summary>
  
## Build and run in a container

</summary>

### Prerequisites:

```sh
sudo pacman -S git docker docker-compose docker-buildx
sudo usermod -aG docker $USER
sudo systemctl enable --now docker.service
git clone https://github.com/pnedkov/ipask.git
cd ipask/
```

### Build and run as a stand-alone container

- Build:

  ```sh
  docker build -t ipask .
  ```

- Run:
  ```sh
  docker run -d -p 8080:8080 ipask
  ```

### Build and run with Docker Compose behind nginx reverse proxy

- Generate a self-signed test key-pair utilized by nginx

  ```sh
  CN=yourdomain.com ./resources/generate_cert.sh
  ```

- Build and run

  ```sh
  docker compose up -d
  ```

</details>
