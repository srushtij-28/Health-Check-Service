from flask import Flask, jsonify
import psutil
from datetime import datetime

app = Flask(__name__)

START_TIME = datetime.now()


@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


@app.route("/ready")
def readiness():
    # Simulate dependency checks
    database_connected = True
    cache_connected = True

    if database_connected and cache_connected:
        return jsonify({
            "status": "READY"
        }), 200

    return jsonify({
        "status": "NOT READY"
    }), 503


@app.route("/live")
def liveness():
    return jsonify({
        "status": "ALIVE"
    })


@app.route("/metrics")
def metrics():
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "uptime_seconds": (
            datetime.now() - START_TIME
        ).total_seconds()
    })


@app.route("/")
def home():
    return jsonify({
        "message": "Health Check Service Running"
    })


if __name__ == "__main__":
    app.run(debug=True)
