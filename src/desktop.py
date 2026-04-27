import threading
import time

import uvicorn
import webview

from server import app


def start_server() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8094, log_level="warning")


if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1.0)

    webview.create_window("Calculator", "http://127.0.0.1:8094", width=1100, height=760)
    webview.start()
