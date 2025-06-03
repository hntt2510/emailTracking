from flask import Flask, request, redirect, send_file
from flask import Response
from datetime import datetime
import os

app = Flask(__name__)

LOG_DIR = "tracking_logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_event(event_type, email, extra=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] EVENT: {event_type.upper()} | EMAIL: {email}"
    if extra:
        log_line += f" | INFO: {extra}"
    print(log_line)
    with open(os.path.join(LOG_DIR, "tracking.log"), "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

@app.route("/open")
def track_open():
    email = request.args.get("email", "unknown")
    log_event("open", email)
    gif_path = os.path.join(LOG_DIR, "pixel.gif")
    if not os.path.exists(gif_path):
        with open(gif_path, "wb") as f:
            f.write(
                b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!"
                b"\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01"
                b"\x00\x00\x02\x02L\x01\x00;"
            )
    return send_file(gif_path, mimetype="image/gif")

@app.route("/click")
def track_click():
    email = request.args.get("email", "unknown")
    target_url = request.args.get("target")
    if not target_url:
        return "Missing target URL", 400

    if "infoasia.com.vn" in target_url:
        link_name = "link1"
    elif "zalo.me" in target_url:
        link_name = "link2"
    else:
        link_name = "other"

    log_event("click", email, f"{link_name} -> {target_url}")
    return redirect(target_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


    
@app.route("/log")
def view_log():
    try:
        with open(os.path.join(LOG_DIR, "tracking.log"), "r", encoding="utf-8") as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except:
        return "No log found."

@app.route("/download_log")
def download_log():
    return send_file(os.path.join(LOG_DIR, "tracking.log"), as_attachment=True)