from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return (
        "Hello World from GCP Compute instance with Docker Image containing simple Flask app 15939"
        "Paweł Grabacki"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
