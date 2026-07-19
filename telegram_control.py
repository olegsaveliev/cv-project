import os, sys, time, subprocess, requests

# --- config ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = str(os.environ.get("TELEGRAM_CHAT_ID", ""))
API = f"https://api.telegram.org/bot{TOKEN}"
HERE = os.path.dirname(os.path.abspath(__file__))

# a command -> the detector script (plus any args) it launches
DETECTORS = {
    "/start":  ["detect_alert.py"],              # photo alerts, all objects
    "/people": ["detect_alert.py", "--people"],  # photo alerts, people only
    "/clip":   ["detect_clip.py"],               # short video clips
    "/stream": ["detect_stream.py"],             # live browser view + alerts
}

HELP = (
    "🤖 Camera controller\n"
    "/start – photo alerts (everything)\n"
    "/people – photo alerts, people only\n"
    "/clip – video-clip alerts\n"
    "/stream – live view + alerts\n"
    "/stop – stop the camera\n"
    "/status – is it running?\n"
    "/help – this message"
)

current = None      # the running detector subprocess (or None)


def send(text):
    try:
        requests.post(f"{API}/sendMessage",
                      data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")


def running():
    return current is not None and current.poll() is None


def stop_detector():
    global current
    if running():
        current.terminate()             # ask it to stop
        try:
            current.wait(timeout=5)
        except subprocess.TimeoutExpired:
            current.kill()               # force it if it won't
    current = None


def start_detector(script_args):
    global current
    stop_detector()                      # only one camera user at a time
    # same Python (venv) + same env (TELEGRAM_* already loaded), run in this folder
    current = subprocess.Popen([sys.executable] + script_args, cwd=HERE)


def handle(cmd):
    if cmd in DETECTORS:
        script_args = DETECTORS[cmd]
        start_detector(script_args)
        send(f"🟢 Started: {' '.join(script_args)}")
    elif cmd == "/stop":
        if running():
            stop_detector()
            send("🔴 Camera stopped.")
        else:
            send("💤 Nothing was running.")
    elif cmd == "/status":
        send("✅ Camera is running." if running() else "💤 Idle.")
    else:
        send(HELP)


def latest_offset():
    """Skip any commands sent while the controller was offline."""
    try:
        r = requests.get(f"{API}/getUpdates", params={"timeout": 0}, timeout=15)
        updates = r.json().get("result", [])
        if updates:
            return updates[-1]["update_id"] + 1
    except Exception as e:
        print(f"startup drain error: {e}")
    return None


def main():
    if not TOKEN or not CHAT_ID:
        sys.exit("Missing TELEGRAM_TOKEN / TELEGRAM_CHAT_ID — did you load .env?")

    offset = latest_offset()             # ignore old commands on startup
    send("🤖 Controller online. Send /help for commands.")
    print("Controller running. Ctrl+C to quit.")

    try:
        while True:
            try:
                # long-poll Telegram: this call waits up to 30s for a message,
                # so we're not hammering the API. Outbound only — nothing exposed.
                params = {"timeout": 30}
                if offset is not None:
                    params["offset"] = offset
                r = requests.get(f"{API}/getUpdates", params=params, timeout=40)

                for update in r.json().get("result", []):
                    offset = update["update_id"] + 1
                    msg = update.get("message") or {}
                    chat_id = str(msg.get("chat", {}).get("id", ""))
                    if chat_id != CHAT_ID:
                        continue                 # <-- ignore everyone but you
                    text = (msg.get("text") or "").strip()
                    if not text:
                        continue
                    cmd = text.split()[0].split("@")[0].lower()
                    print(f"cmd from you: {cmd}")
                    handle(cmd)
            except requests.exceptions.RequestException as e:
                print(f"poll error: {e}")
                time.sleep(3)
    except KeyboardInterrupt:
        stop_detector()
        send("🤖 Controller offline.")
        print("\nStopped controller (and any running detector).")


if __name__ == "__main__":
    main()
