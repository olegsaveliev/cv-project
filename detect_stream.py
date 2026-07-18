import os, time, threading
import cv2, requests
from flask import Flask, Response
from ultralytics import YOLO

# --- config ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
CONFIDENCE = 0.7        # ignore weak detections
COOLDOWN = 60           # seconds between alerts for the same object
PORT = 8000             # open http://mypi.local:8000 on your laptop

model = YOLO("models/yolo11n.pt")

# --- shared state between the detection thread and the web server ---
latest_jpeg = None          # most recent annotated frame, JPEG-encoded
lock = threading.Lock()     # guards latest_jpeg (two threads touch it)
last_alert = {}             # per-object timestamp for the cooldown


def send_photo(caption, jpeg_bytes):
    """Send an annotated snapshot to Telegram (no disk write needed)."""
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID, "caption": caption},
            files={"photo": ("alert.jpg", jpeg_bytes)},
            timeout=10,
        )
    except Exception as e:
        print(f"Telegram error: {e}")


def detection_loop():
    """Run YOLO forever: publish each frame for the stream, and alert."""
    global latest_jpeg
    for r in model.predict(source=0, stream=True, conf=CONFIDENCE, verbose=False):
        frame = r.plot()                       # annotated frame (numpy array)
        ok, buf = cv2.imencode(".jpg", frame)  # encode once, reuse for both
        if not ok:
            continue
        jpeg = buf.tobytes()

        # 1. publish the frame for the live web stream
        with lock:
            latest_jpeg = jpeg

        # 2. Telegram alert, with a per-object cooldown
        now = time.time()
        seen = {model.names[int(c)] for c in r.boxes.cls}
        for label in seen:
            if now - last_alert.get(label, 0) > COOLDOWN:
                last_alert[label] = now
                send_photo(f"👀 Detected: {label}", jpeg)
                print(f"ALERT: {label}")


# --- the tiny web server ---
app = Flask(__name__)

PAGE = """<!doctype html>
<title>Pi Live Detection</title>
<body style="margin:0;background:#111;text-align:center">
  <h2 style="color:#eee;font-family:sans-serif">🥧 Raspberry Pi — Live Detection</h2>
  <img src="/video" style="max-width:100%;height:auto">
</body>"""


@app.route("/")
def index():
    return PAGE


def mjpeg():
    """Yield the latest frame over and over as an MJPEG stream."""
    while True:
        with lock:
            frame = latest_jpeg
        if frame is not None:
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        time.sleep(0.05)


@app.route("/video")
def video():
    return Response(mjpeg(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    # detection runs in the background; the web server runs in the foreground
    threading.Thread(target=detection_loop, daemon=True).start()
    print(f"Live view:  http://mypi.local:{PORT}   (Ctrl+C to stop)")
    app.run(host="0.0.0.0", port=PORT, threaded=True)
