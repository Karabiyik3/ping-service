"""Tiny HTTP service for the Insider One DevOps case.

Endpoints:
    GET /ping     -> "pong"        (the core requirement)
    GET /healthz  -> {"status":"ok"} (used by Kubernetes liveness/readiness probes)
"""
import logging
import os
import json

from flask import Flask, jsonify

# --- Structured (JSON) logging -------------------------------------------------
# A small touch from the bonus list: emit JSON logs so they're easy to parse.
class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(
            {
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
            }
        )


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])
log = logging.getLogger("ping-service")

app = Flask(__name__)


@app.get("/ping")
def ping():
    """Core endpoint required by the case: returns plain text 'pong'."""
    log.info("ping received")
    return "pong", 200


@app.get("/healthz")
def healthz():
    """Health endpoint for Kubernetes probes."""
    return jsonify(status="ok"), 200


@app.get("/")
def index():
    """Friendly root so visitors to the public URL see something useful."""
    return jsonify(
        service="ping-service",
        endpoints=["/ping", "/healthz"],
    ), 200


if __name__ == "__main__":
    # PORT can be overridden via env var; defaults to 8080.
    port = int(os.environ.get("PORT", "8080"))
    log.info("starting ping-service on port %s", port)
    app.run(host="0.0.0.0", port=port)
