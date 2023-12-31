from flask import Flask, request, render_template
import os


with open(
    os.path.join(os.path.realpath(os.path.dirname(__file__)), "VERSION")
) as version_file:
    app_version = version_file.read().strip()


app = Flask(__name__)


def format_headers(headers):
    return "<br>".join(f"{key}: {value}" for key, value in headers.items())


def get_client_ip():
    xff_ip = request.headers.get("X-Forwarded-For")

    return xff_ip if xff_ip else request.headers.get("X-Real-IP", request.remote_addr)


@app.route("/")
def home():
    client_ip = get_client_ip()
    user_agent = request.headers.get("User-Agent", "").lower()

    if "mozilla" in user_agent or "chrome" in user_agent or "safari" in user_agent:
        client_info = {
            "ip": client_ip,
            "xff": request.headers.get("X-Forwarded-For"),
            "user_agent": user_agent,
            "headers": format_headers(request.headers),
            "remote_hostname": request.host,
            "city": None,
            "country": None,
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
    return f"{request.headers.get('Host')}\n"


@app.route("/xff")
def return_xff():
    return f"{request.headers.get('X-Forwarded-For')}\n"


@app.route("/city")
def return_city():
    return "None\n"


@app.route("/country")
def return_country():
    return "None\n"


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
