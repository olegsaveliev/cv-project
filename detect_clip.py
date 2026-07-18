import os, time, subprocess, requests
import cv2
from ultralytics import YOLO

# --- config ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
CONFIDENCE = 0.7        # ignore weak detections
COOLDOWN = 60           # seconds between clips, so it doesn't spam
TARGET = "person"       # which object triggers a clip
CLIP_FRAMES = 24        # annotated frames to capture (~6-7s at ~3.4 FPS)

# clips are kept on the Pi as "latest only" (overwritten each time):
#   videos/raw/   -> the raw OpenCV clip
#   videos/final/ -> the H.264 clip that gets sent to Telegram
RAW_PATH = "videos/raw/clip_raw.mp4"
FINAL_PATH = "videos/final/clip.mp4"
os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)
os.makedirs(os.path.dirname(FINAL_PATH), exist_ok=True)

model = YOLO("models/yolo11n.pt")


def send_text(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                      data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")


def send_clip(frames, elapsed):
    """Stitch annotated frames into an H.264 mp4 and send it to Telegram."""
    if not frames:
        return
    h, w = frames[0].shape[:2]
    # play the clip at the real capture rate (clamped to a sane range)
    fps = max(1.0, min(15.0, len(frames) / max(elapsed, 0.001)))

    # 1. OpenCV writes the raw clip
    raw = RAW_PATH
    writer = cv2.VideoWriter(raw, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    for f in frames:
        writer.write(f)
    writer.release()

    # 2. ffmpeg re-encodes to H.264 so Telegram plays it inline
    out = FINAL_PATH
    subprocess.run(
        ["ffmpeg", "-y", "-i", raw, "-c:v", "libx264",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
        check=True, capture_output=True,
    )

    # 3. send it
    try:
        with open(out, "rb") as v:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVideo",
                          data={"chat_id": CHAT_ID,
                                "caption": f"🎥 {TARGET} detected"},
                          files={"video": v}, timeout=60)
    except Exception as e:
        print(f"Telegram error: {e}")
    print(f"Sent clip: {len(frames)} frames @ {fps:.1f} FPS")


send_text("🟢 Clip detector started")
print("Running. Ctrl+C to stop.")

recording = None        # None, or {"frames": [...], "start": t}
last_clip = 0

try:
    for r in model.predict(source=0, stream=True, conf=CONFIDENCE, verbose=False):
        now = time.time()
        seen = {model.names[int(c)] for c in r.boxes.cls}
        frame = r.plot()                        # annotated frame, in memory

        if recording is not None:
            # currently capturing a clip
            recording["frames"].append(frame)
            if len(recording["frames"]) >= CLIP_FRAMES:
                send_clip(recording["frames"], now - recording["start"])
                last_clip = now
                recording = None
        elif TARGET in seen and now - last_clip > COOLDOWN:
            # trigger a new clip
            print(f"{TARGET} detected — recording {CLIP_FRAMES} frames...")
            recording = {"frames": [frame], "start": now}
except KeyboardInterrupt:
    send_text("🔴 Clip detector stopped")
    print("\nStopped.")
