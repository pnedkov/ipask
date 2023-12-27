from flask import Flask, request, render_template
from urllib.parse import urlparse
import os
import requests


with open(
    os.path.join(os.path.realpath(os.path.dirname(__file__)), "VERSION")
) as version_file:
    app_version = version_file.read().strip()


app = Flask(__name__)
ip_api = os.getenv("IP_API", "False").lower() == "true"


def format_headers(headers):
    return "<br>".join(f"{key}: {value}" for key, value in headers.items())


# TODO: Store all ip-api.com json fields in a dictionary
def get_country(ip):
    ip_api_location = None
    try:
        if ip_api:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            json_response = response.json()
            country = json_response.get("country")
            region_name = json_response.get("regionName")
            city = json_response.get("city")
            ip_api_location = (
                f"{country}, {region_name}, {city}" if country is not None else None
            )

        return ip_api_location
    except requests.RequestException:
        return "N/A"


@app.route("/")
def home():
    client_ip = request.headers.get("X-Real-IP", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "").lower()

    if "mozilla" in user_agent or "chrome" in user_agent or "safari" in user_agent:
        client_info = {
            "ip": client_ip,
            "remote_hostname": urlparse("//" + str(request.headers.get("Host"))).netloc,
            "x_forwarded_for": request.headers.get("X-Forwarded-For"),
            "country": get_country(client_ip),
            "user_agent": request.user_agent.string,
            "headers": format_headers(request.headers),
        }
        return render_template(
            "index.html",
            client_info=client_info,
            ip_api=ip_api,
            app_version=app_version,
        )

    return f"{client_ip}\n"


@app.route("/ip")
def return_ip():
    return f"{request.headers.get('X-Real-IP', request.remote_addr)}\n"


@app.route("/host")
def return_host():
    return f"{request.headers.get('Host')}\n"


@app.route("/xff")
def return_xff():
    return f"{request.headers.get('X-Forwarded-For')}\n"


@app.route("/country")
def return_country():
    return f"{get_country(request.headers.get('X-Real-IP', request.remote_addr))}\n"


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
