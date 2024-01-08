from flask import Flask, request, render_template
import os
import socket
import subprocess
import geoip2.database


#
# Gets the application version from the git repository
# git describe --always --long
#
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


#
# Gets an environment variable and converts it to bool
#
def get_env_bool(env_var, default_value):
    return bool(
        os.getenv(env_var, default_value).lower()
        in ["1", "on", "yes", "yup", "yeah", "true", "enable", "enabled", "certainly"]
    )


# set the 'geoip' toggle
geoip = get_env_bool("GEOIP", "false")

# set the 'reverse_dns_lookup' toggle
reverse_dns_lookup = get_env_bool("REVERSE_DNS_LOOKUP", "false")


#
# Gets the client's IP address
#
def get_client_ip():
    xff_ip = request.headers.get("X-Forwarded-For")

    return xff_ip if xff_ip else request.headers.get("X-Real-IP", request.remote_addr)


#
# Gets the client's FQDN via reverse DNS lookup
#
def get_client_host(ip):
    c_host = None

    if ip and reverse_dns_lookup:
        try:
            c_host = socket.gethostbyaddr(str(ip))[0]
        except Exception:
            pass

    return c_host


#
# Gets the client's GeoIP data from a local database file
#
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


#
# Converts all HTTP headers in a HTML format
#
def format_headers(headers):
    return "<br>".join(f"{key}: {value}" for key, value in headers.items())


#
# / route
# Returns the Home page when viewed from a browser
# and the client's IP address when accessed via
# command line (curl, wget)
#
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


#
# /ip route
# Returns the client's IP address
#
@app.route("/ip")
def return_ip():
    return f"{get_client_ip()}\n"


#
# /home route
# Returns the client's FQDN
#
@app.route("/host")
def return_host():
    c_ip = str(get_client_ip())
    return f"{get_client_host(c_ip)}\n"


#
# /xff route
# Returns the X-Forwarded-For request header
#
@app.route("/xff")
def return_xff():
    return f"{request.headers.get('X-Forwarded-For')}\n"


#
# /city route
# Returns the client's city according to the local GeoIP database
#
@app.route("/city")
def return_city():
    c_ip = get_client_ip()
    c_geo = get_client_geo(c_ip)
    c_geo_city = c_geo.get("city")
    return f"{c_geo_city}\n"


#
# /country route
# Returns the client's country according to the local GeoIP database
#
@app.route("/country")
def return_country():
    c_ip = get_client_ip()
    c_geo = get_client_geo(c_ip)
    c_geo_country = c_geo.get("country")
    return f"{c_geo_country}\n"


#
# /ua route
# Returns the client's User-Agent header
#
@app.route("/ua")
def return_ua():
    return f"{request.user_agent.string}\n"


#
# /headers route
# Returns all client's HTTP headers
#
@app.route("/headers")
def return_headers():
    return dict(request.headers)


#
# Default '404' response
#
@app.errorhandler(404)
def page_not_found(e):
    return f"{e}\n", 404


#
# Main
#
if __name__ == "__main__":
    app.run()
