from __future__ import annotations

import os
import signal
import socket
import subprocess
import time
import tomllib
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

API_ROOT = Path(__file__).parents[1]
RAILWAY_CONFIG = API_ROOT / "railway.toml"
EXPECTED_START_COMMAND = (
    "sh -c 'exec uvicorn app.main:app --host 0.0.0.0 --port \"$PORT\"'"
)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def test_railway_start_command_expands_port_and_serves_health() -> None:
    with RAILWAY_CONFIG.open("rb") as config_file:
        config = tomllib.load(config_file)

    assert config["build"]["builder"] == "RAILPACK"
    assert config["deploy"]["healthcheckPath"] == "/health"
    start_command = config["deploy"]["startCommand"]
    assert start_command == EXPECTED_START_COMMAND

    port = _free_port()
    assert port != 8000
    environment = os.environ.copy()
    environment.update(
        {
            "PORT": str(port),
            "ALLOWED_ORIGINS": "https://usmora.vercel.app",
        }
    )
    process = subprocess.Popen(
        ["/bin/sh", "-c", start_command],
        cwd=API_ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )

    try:
        deadline = time.monotonic() + 10
        response = None
        while time.monotonic() < deadline:
            if process.poll() is not None:
                break
            try:
                response = urlopen(
                    Request(
                        f"http://127.0.0.1:{port}/health",
                        headers={"Origin": "https://usmora.vercel.app"},
                    ),
                    timeout=1,
                )
                break
            except URLError:
                time.sleep(0.1)

        if response is None:
            stdout, stderr = process.communicate(timeout=2)
            raise AssertionError(
                "Railway start command did not serve /health.\n"
                f"stdout={stdout}\n"
                f"stderr={stderr}"
            )

        assert response.status == 200
        assert response.read() == b'{"status":"ok"}'
        assert response.headers["access-control-allow-origin"] == "https://usmora.vercel.app"
    finally:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.communicate()
