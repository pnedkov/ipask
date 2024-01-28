# IP Ask

`whatsmyip` type of web application written in Python with Flask framework

[ipask.me](https://ipask.me)

---

<details>
<summary>
  
## Getting started

</summary>

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

</details>

---

<details>
<summary>
  
## Run from the source code

</summary>

- Environment variables:
  | Environment variable | Default value |
  | --- | --- |
  | GEOIP | `false` |
  | REVERSE_DNS_LOOKUP | `false` |

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
  
## Run in a stand-alone container

</summary>

- Prerequisites:

  ```sh
  sudo pacman -S docker docker-compose docker-buildx
  sudo usermod -aG docker $USER
  sudo systemctl enable --now docker.service
  ```

- Build:

  ```sh
  docker build -t ipask .
  ```

- Run:
  ```sh
  docker run -d -p 8080:8080 ipask
  ```

</details>

---

<details>
<summary>
  
## Run with Docker Compose behind nginx reverse proxy

</summary>
      
* Generate a self-signed test key-pair utilized by the nginx reverse proxy.
  
  Review the environment variables inside `resources/generate_cert.sh` and set them accordingly.
  For example:
  ```sh
  CN=yourdomain.com ./resources/generate_cert.sh
  ```
  Or you could use your own key and certificate. `docker-compose.yaml` expects to find them here:
  - $HOME/.nginx/key.pem
  - $HOME/.nginx/cert.pem

- (Option A): Pull the latest container version from hub.docker.com and run it:
  ```sh
  docker compose -f docker-compose.yaml up -d
  ```
- (Option B): Build the container from the source and run it:
  ```sh
  docker compose up -d
  ```
  Use the `--build` option in order to force the build process in case you already have the `ipask` container and want a new one.

</details>

---

<details>
<summary>
  
## Usage

</summary>

- If running `ipask` as a stand-alone application:

  ```sh
  $ curl <host>:8080
  $ wget -qO - <host>:8080
  ```

  Or navigate to `http://<host>:8080` from your browser.

- If runing `ipask` with nginx reverse proxy:

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
