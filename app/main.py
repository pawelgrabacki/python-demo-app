import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    build_number = os.getenv("BUILD_NUMBER", "unknown")

    return f"""
    <html>
        <head><title>python-demo-app</title></head>
        <body>
            <h1>Hello from Flask</h1>

            <h3>
              Hello World from GCP Compute instance with Docker Image containing simple Python/Flask app
              <br>
              Paweł Grabacki - 15939
            </h3>

            <p><b>Jenkins Build Number:</b> {build_number}</p>

            <p>This is HTML returned directly from main.py</p>

            <ul>
              <li><a href="https://github.com/pawelgrabacki/python-demo-app">
                github/pawelgrabacki/python-demo-app
              </a></li>

              <li><a href="https://hub.docker.com/r/pawelgrabacki/python-demo-app">
                dockerhub/pawelgrabacki/python-demo-app
              </a></li>
            </ul>
            <p>Update #1<p>



        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
