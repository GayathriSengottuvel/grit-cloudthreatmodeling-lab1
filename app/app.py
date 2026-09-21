import os
import subprocess
from uuid import uuid4

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify(
        service="cloud-threat-modeling-demo",
        message="CI/CD security lab application",
        environment=os.getenv("APP_ENV", "local"),
    )


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/uuid")
def generate_uuid():
    return jsonify(uuid=str(uuid4()))


@app.get("/run-check")
def run_check():
    """
    INTENTIONALY INSECURE TRAINING EXAMPLE.

    The user-controlled 'cmd' value is passed to a shell.
    Bandit should flag this as a shell-injection risk.

    Do not use this pattern in production.
    """
    cmd = request.args.get("cmd", "echo training")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return jsonify(output=result.stdout.strip())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
