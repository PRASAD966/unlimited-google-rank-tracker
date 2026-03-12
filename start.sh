#!/bin/bash
# start.sh - Production startup for rankplex.cloud (Flask-SocketIO with threading mode)
# Playwright requires headless display on Linux - Xvfb provides it.

# ── 1. Virtual Display for headless Playwright ──────────────────────────────
Xvfb :99 -screen 0 1280x1024x24 &
XVFB_PID=$!
export DISPLAY=:99

# Optional: lightweight window manager (helps Playwright render pages correctly)
fluxbox &

# Optional: VNC for remote debugging (remove in locked-down prod if not needed)
# x11vnc -display :99 -forever -shared -rfbport 5900 -nopw &

# ── 2. Launch Application ────────────────────────────────────────────────────
if [ "$FLASK_ENV" = "production" ]; then
    echo "Starting in PRODUCTION mode..."
    # IMPORTANT: Flask-SocketIO with async_mode=threading MUST run with:
    #   -w 1       (single worker — SocketIO rooms/state are in-process)
    #   --worker-class gthread  (thread-based, compatible with threading mode)
    #   --threads  (thread pool for concurrent requests)
    # Do NOT use gevent/eventlet workers — they break Playwright sync API
    gunicorn \
        --worker-class gthread \
        --threads 50 \
        -w 1 \
        --bind 0.0.0.0:8000 \
        --timeout 600 \
        --keep-alive 75 \
        --log-level info \
        --access-logfile - \
        --error-logfile - \
        "server:app"
else
    echo "Starting in DEVELOPMENT mode..."
    python server.py --port 8000
fi
