"""
House Price Prediction Web Application
Entry point for running the machine learning property valuation service.
"""
import os
import sys
import threading
import webbrowser
import time
from flask_app import app


def run_app():
    port = int(os.environ.get("PORT", 5000))
    print("=" * 60)
    print("  HOUSE PRICE PREDICTION: MACHINE LEARNING WEB APP")
    print(f"  Access URL: http://127.0.0.1:{port}")
    print("=" * 60)

    def _open_browser():
        time.sleep(1.5)
        webbrowser.open(f"http://127.0.0.1:{port}")

    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    run_app()