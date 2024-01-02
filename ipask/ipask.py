from flask import Flask, request, render_template
import os
import socket
import subprocess
import geoip2.database


def get_app_version():
    ver = "v0.0.0-0-ga1b2c3d4"

    try:
        ver = (
            subprocess.check_output(["git", "describe", "--always", "--long"])
            .strip()
            .decode()
        )
    except Exception:
        pass

    return ver


app = Flask(__name__)
app_version = get_app_version()


def get_env_bool(env_var, default_value):
    return bool(
        os.getenv(env_var, default_value).lower()
        in ["1", "on", "yes", "yup", "yeah", "true", "enable", "enabled", "certainly"]
    )


geoip = get_env_bool("GEOIP", "false")
reverse_dns_lookup = get_env_bool("REVERSE_DNS_LOOKUP", "false")


def get_client_ip():
    xff_ip = request.headers.get("X-Forwarded-For")

    return xff_ip if xff_ip else request.headers.get("X-Real-IP", request.remote_addr)


def get_client_host(ip):
    c_host = None

    if ip and reverse_dns_lookup:
        try:
            c_host = socket.gethostbyaddr(str(ip))[0]
        except Exception:
            pass

    return c_host


def get_client_geo(ip):
    c_city = c_country = None

    if geoip:
        try:
            geo_reader = geoip2.database.Reader("resources/GeoLite2-City.mmdb")
        except Exception:
            pass
        else:
            try:
                geo_response = geo_reader.city(ip)
            except Exception:
                pass
            else:
                c_city = geo_response.city.name
                c_country = geo_response.country.name

    c_geo = {"city": c_city, "country": c_country}

    return c_geo


def format_headers(headers):
    return "<br>".join(f"{key}: {value}" for key, value in headers.items())


@app.route("/")
def home():
    client_ip = get_client_ip()
    client_ua = request.user_agent.string

    if "Mozilla" in client_ua or "Chrome" in client_ua or "Safari" in client_ua:
        client_geo = get_client_geo(client_ip)
        client_city = client_geo.get("city")
        client_country = client_geo.get("country")

        client_info = {
            "ip": client_ip,
            "host": get_client_host(client_ip),
            "xff": request.headers.get("X-Forwarded-For"),
            "user_agent": client_ua,
            "headers": format_headers(request.headers),
            "city": client_city,
            "country": client_country,
            "server_host": request.host,
        }

        return render_template(
            "index.html",
            client_info=client_info,
            app_version=app_version,
        )

    return f"{client_ip}\n"


@app.route("/ip")
def return_ip():
    return f"{get_client_ip()}\n"


@app.route("/host")
def return_host():
    c_ip = str(get_client_ip())
    return f"{get_client_host(c_ip)}\n"


@app.route("/xff")
def return_xff():
    return f"{request.headers.get('X-Forwarded-For')}\n"


@app.route("/city")
def return_city():
    c_ip = get_client_ip()
    c_geo = get_client_geo(c_ip)
    c_geo_city = c_geo.get("city")
    return f"{c_geo_city}\n"


@app.route("/country")
def return_country():
    c_ip = get_client_ip()
    c_geo = get_client_geo(c_ip)
    c_geo_country = c_geo.get("country")
    return f"{c_geo_country}\n"


@app.route("/ua")
def return_ua():
    return f"{request.user_agent.string}\n"


@app.route("/headers")
def return_headers():
    return dict(request.headers)


@app.errorhandler(404)
def page_not_found(e):
    return f"{e}\n", 404


if __name__ == "__main__":
    app.run()
