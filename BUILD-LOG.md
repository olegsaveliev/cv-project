# Build Log

> A running record of the build — progress against the plan, decisions made, and the problems solved along the way. It complements [`DESIGN.md`](./DESIGN.md) (*why* the choices were made) and [`README.md`](./README.md) (how to reproduce the build). The "Engineering notes" section at the end doubles as a debugging reference for anyone reproducing this project.

---

## Current status

- **v1 base + alerting: complete.** Live detection runs on the Pi, with Telegram photo alerts, a per-object cooldown, and a tuned confidence threshold. The README documents the full stack with an architecture diagram.
- **Next:** choose the custom object → collect 50–150 photos → label in Roboflow → train on Colab → deploy `best.pt`. Remaining polish: record the demo GIF and fill in the personal "what I learned" section.

### Environment reference
- Host: `mypi` (`mypi.local`) · project at `/home/oleg/cv-project` · branch `main`
- Activate the environment: `source ~/cv-project/venv/bin/activate`
- Run the detector: `set -a && source .env && set +a && python detect_alert.py`

### Measured performance
- ~290–320 ms inference per frame on the Pi 5 CPU ≈ **3–3.4 FPS**.
- True detections score 0.87–0.93; a false positive scored ~0.59 — hence the 0.7 confidence threshold.

---

## Progress against the plan

### Phase 1 — Hardware & OS
- [x] Hardware assembled (Pi 5, official case + fan, 27W supply, 32GB A2 card)
- [x] OS flashed to microSD (Raspberry Pi Imager; Wi-Fi + SSH configured before first boot)
- [x] First boot, joined Wi-Fi, reachable on the network, SSH login working
- [x] `sudo apt update && full-upgrade` completed; locale warnings resolved

### Phase 2 — Remote workflow
- [x] VS Code + Remote-SSH connected from the laptop to the Pi
- [x] `~/cv-project` created and opened in VS Code

### Phase 3 — Camera
- [x] Logitech C270 connected (USB 3.0), confirmed via `lsusb` and `/dev/video0`
- [x] Test capture succeeded (`fswebcam test.jpg`)

### Phase 4 — Generic detection (v1 base)
- [x] `venv` created; `ultralytics` installed (ultralytics 8.4.100, torch 2.13.0, opencv 5.0.0.93)
- [x] Still-image detection works — `yolo predict model=yolo11n.pt source=bus.jpg` → 4 persons, 1 bus, 320 ms
- [x] Project structure created (`models/`, `docs/`, `data/`, `requirements.txt`, `.gitignore`)
- [x] Git initialized, first commits made, pushed to GitHub (`main`)
- [x] Live camera detection works (`detect_live.py`) — ~290 ms/frame, reliably detects a person

### Phase 4b — Alerting (Telegram)
- [x] Telegram bot created via @BotFather; chat ID obtained
- [x] Credentials stored in `.env` (gitignored)
- [x] `detect_alert.py` sends annotated snapshots on detection
- [x] Per-object cooldown (60 s) prevents spam at ~3.4 FPS
- [x] Confidence threshold tuned to 0.7 (removed a 0.59 false positive)
- [ ] Autostart on boot (systemd service) — deferred

### Phase 4c — Documentation
- [x] README architecture section with a Mermaid flowchart (live loop + offline training path)
- [x] README stack table — every layer and where it runs
- [x] README section on Telegram alerting, cooldown rationale, and confidence tuning
- [ ] Demo GIF recorded and added to `docs/`
- [ ] Personal "what I learned / tradeoffs" section filled in

### Phase 5 — Custom object
- [ ] Custom object chosen
- [ ] 50–150 images collected
- [ ] Images labeled in Roboflow, exported in YOLO format
- [ ] Trained on Google Colab → `best.pt`
- [ ] `best.pt` deployed to the Pi; custom detection confirmed

### Phase 6 — Publish v1
- [ ] README polished with steps, bill of materials, and "what I learned"
- [ ] Demo GIF/video recorded
- [ ] MIT license added
- [ ] Pushed to GitHub

### Phase 7 — v2 (optional): AI Camera / IMX500
- [ ] AI Camera connected; `imx500` tooling installed
- [ ] Pre-packaged on-sensor demo runs
- [ ] Custom model exported to IMX format and packaged to `.rpk`
- [ ] Custom `.rpk` runs on-sensor and is documented

---

## Decision log

- **Pi 5, not Pi 4** — better CPU for inference, and the target platform for the AI Camera.
- **4GB/8GB, not 16GB** — extra RAM does not speed up detection; the CPU is the bottleneck.
- **Official case + built-in fan** — reliable cooling without the throttling risk of an Active Cooler inside the official case.
- **USB webcam for v1, AI Camera (IMX500) for v2.**
- **Train on Colab, never on the Pi** — the Pi is too slow for training.
- **Edit on the laptop, run on the Pi** — VS Code + Remote-SSH, headless Pi.
- **Confidence threshold 0.7** — cut a false positive at 0.59 without losing true detections.
- **Per-object cooldown (60 s)** — turns a firehose of frames into usable notifications.

---

## Engineering notes & gotchas

Real problems hit during the build and how they were solved — useful if you're reproducing it.

**Networking & first login**
- **`.local` is slow to resolve on first boot.** Give the Pi a few minutes, then find it by IP: broadcast-ping the subnet and read `arp -a`, or check the router's connected-devices list.
- **Confirm a candidate IP isn't your own machine.** A host pinging itself replies in ~0.7 ms; on macOS verify with `ipconfig getifaddr en0` before trying to SSH.
- **The username is whatever you set in Imager**, not your laptop's username. If unsure, read it from the card: `cat /Volumes/bootfs/user-data` (and `network-config` to verify the Wi-Fi SSID and country code).
- **Locale warnings on login** (`LC_CTYPE: cannot change locale`) are harmless. Clear them by generating the locale on the Pi: uncomment `en_US.UTF-8` in `/etc/locale.gen`, then `sudo locale-gen && sudo update-locale`.

**Hardware**
- **Plug the fan into the J17 header while the case lid is still open** — the connector is hard to reach once the lid is on.

**Git & GitHub**
- **`git init` defaults to `master`; GitHub expects `main`.** Run `git branch -M main` before the first push.
- **GitHub rejects account passwords over HTTPS.** Use a Personal Access Token (Settings → Developer settings → Personal access tokens → classic → `repo` scope) as the password.
- **VS Code can hijack Git credential prompts over SSH.** `GIT_ASKPASS` points at a VS Code socket that fails remotely (`ECONNREFUSED`). Fix: `unset GIT_ASKPASS VSCODE_GIT_IPC_HANDLE` before pushing.

**VS Code Remote-SSH**
- **Extensions that touch project files must be installed on the *remote* (Pi) side** — look for "Install in SSH: mypi.local", or they stay disabled in the workspace.
- **Know which window is which.** With one local and one remote window open, confirm the green indicator (bottom-left) and that the terminal prompt reads `oleg@mypi` before running project commands.

**YOLO / inference**
- **`pip install ultralytics` pulls in `nvidia-*` CUDA packages** as PyTorch dependencies. The Pi has no NVIDIA GPU, so they sit unused — harmless, just disk space.
- **Headless means no preview window.** With no monitor, YOLO can't use `show=True`; use `save=True` (writes annotated frames to `runs/detect/`) and print labels instead.
- **`Ctrl+C` during live detection prints a long traceback** — that's the interrupt landing mid-inference, not a crash.
- **The C270 reports 30 FPS input, but YOLO processes ~3.4 FPS.** The camera isn't the bottleneck; the Pi's CPU is.

**Telegram alerting**
- **The API URL glues `bot` to the token:** `api.telegram.org/bot<TOKEN>/...`. Omitting the `bot` prefix returns 404.
- **`getUpdates` returns an empty result until you message the bot first** — a bot can't initiate a conversation.
- **Don't prefix a literal token with `$` in a shell command** — `bot$8643...` makes bash expand `$8`, mangling the token. Reference it as a real variable (`$TELEGRAM_TOKEN`) or paste it with no `$`.
- **Environment variables don't persist across terminals** — re-run `set -a && source .env && set +a` in each new shell.
- **Secrets discipline:** credentials live only in `.env` (gitignored) — never in commands or committed files. Rotate any credential the moment it is exposed anywhere.

**Mermaid diagrams (GitHub rendering)**
- **Periods inside dotted-arrow labels break the parser.** `BEST -.replaces yolo11n.pt.-> YOLO` fails because `-.` and `.->` are structural syntax. Use the pipe form `-.->|label text|`.
- **Parentheses inside `subgraph` titles break the parser — even when quoted.** Subgraph titles tokenize more strictly than node labels. Use em-dashes or commas instead: `subgraph device["On the Raspberry Pi 5 — edge"]`.
- **GitHub caches rendered markdown.** After pushing a README fix, hard-refresh (`Cmd+Shift+R`) or the old render persists.
