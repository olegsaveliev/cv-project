# MEMORY.md

> **What this file is:** the project's living memory. Claude Code updates it at the end of every session so the next one starts exactly where we left off. If `PROJECT-CONTEXT.md` is *the plan*, this file is *where we are against the plan*.
>
> **How to update it:** tick boxes as steps complete, fill in "Next step," and append to the Decision log / Gotchas log whenever something is decided or goes wrong-then-fixed. Keep entries short and dated.

---

## Where we are right now
- **Current phase:** ✅ **v1 base COMPLETE.** Webcam (Logitech C270) working, live detection running on the Pi — correctly detects "1 person" continuously at ~290ms/frame (**~3.4 FPS**).
- **Next step:** Choose the custom object → collect 50–150 photos → label in Roboflow → train on Colab → deploy `best.pt`. Also: record demo GIF for the README.
- **Camera status:** ✅ Arrived and confirmed working. `lsusb` shows `Logitech, Inc. Webcam C270`, device at `/dev/video0`.
- **Key facts:** hostname `mypi` → `mypi.local` · username **`oleg`** · project at `/home/oleg/cv-project` · GitHub: https://github.com/olegsaveliev/cv-project · branch `main` · venv: `source ~/cv-project/venv/bin/activate`
- **Measured baseline:** ~290–320ms inference on Pi 5 CPU ≈ **3–3.4 FPS** live. Honest README number.
- **Headless note:** no monitor on the Pi, so `show=True` can't open a window. `detect_live.py` uses `save=True` + printed labels instead.
- **Last updated:** (set this each session)

---

## Status against the plan

### Phase 0 — Planning
- [x] Project defined (Pi 5 object detector → custom object → GitHub)
- [x] Hardware decided (see PROJECT-CONTEXT.md)
- [x] Workflow decided (VS Code + Remote-SSH from MacBook)
- [x] AI stack decided (YOLO + Roboflow + Colab)
- [x] File structure set up (CLAUDE / PROJECT-CONTEXT / MEMORY / guide / README)

> **Legend:** ✅ doable now (no webcam needed) · 📷 needs the Logitech webcam (blocked until it arrives)

### Phase 1 — Hardware & OS
- [x] Hardware ordered
- [x] Hardware arrived *(all except Logitech webcam — still in transit)*
- [x] ✅ OS flashed to microSD (Raspberry Pi Imager on Mac; Wi-Fi + SSH set in Imager)
- [x] ✅ Case assembled with active cooler (fan plugged into J17 FAN header before closing lid)
- [x] ✅ Pi first boot + on Wi-Fi
- [x] ✅ Pi reachable on the network (found via `ping mypi.local` → IP)
- [x] ✅ SSH login works (`ssh oleg@mypi.local`)
- [x] ✅ `sudo apt update && full-upgrade` completed
- [x] ✅ Locale warning addressed (locales generated; residual cosmetic warning ignored — harmless)

### Phase 2 — Remote workflow
- [x] ✅ VS Code + Remote-SSH connected from MacBook to Pi
- [x] ✅ `~/cv-project` folder created and opened in VS Code
- [x] ✅ Five `.md` files copied into `~/cv-project`
- [ ] ✅ Claude Code reads `CLAUDE.md` at session start
- [ ] ✅ (Optional) SSH key set up so no password each time

### Phase 3 — Camera
- [x] 📷 Camera connected (Logitech C270 into a blue USB 3.0 port)
- [x] 📷 Camera confirmed working (`lsusb` → C270; `/dev/video0` present; `fswebcam test.jpg` captured an image)

### Phase 4 — Generic detection (v1 base)
- [x] ✅ `venv` created, `ultralytics` installed (ultralytics 8.4.100, torch 2.13.0, opencv 5.0.0.93)
- [x] ✅ Still-image detection works — `yolo predict model=yolo11n.pt source=bus.jpg` → 4 persons, 1 bus, 320.3ms
- [x] ✅ Project structure created (`models/`, `docs/`, `data/`, `requirements.txt`, `.gitignore`)
- [x] ✅ Git initialized, first commits made, pushed to GitHub (`main` branch)
- [x] 📷 Live camera detection works (`detect_live.py`) — ~290ms/frame, detects "1 person" reliably

### Phase 5 — Custom object (the showcase)
- [ ] ✅ Custom object chosen: __________
- [ ] ✅ 50–150 images collected *(phone photos — can start now)*
- [ ] ✅ Images labeled in Roboflow, exported YOLO format
- [ ] ✅ Trained on Google Colab → got `best.pt`
- [ ] 📷 `best.pt` copied to Pi, `detect_live.py` points at it, custom detection works *(final check needs webcam)*

### Phase 6 — Publish v1
- [ ] README polished with steps + bill of materials + "what I learned"
- [ ] Demo GIF/video recorded
- [ ] MIT license added
- [ ] Pushed to GitHub

### Phase 7 — v2 (optional): AI Camera / IMX500
- [ ] AI Camera connected, `imx500-all`/`imx500-tools` installed
- [ ] Pre-packaged on-sensor demo runs
- [ ] Custom model exported to IMX (`format="imx"`) and packaged to `.rpk`
- [ ] Custom `.rpk` runs on-sensor
- [ ] v2 documented and published

---

## Decision log
> Append dated one-liners when something is decided. (Seed entries from planning below.)
- Pi 5 chosen (not Pi 4) — AI Camera targets Pi 5; better CPU for detection.
- 8GB (or 4GB) kit, **not** 16GB — extra RAM does not speed up detection.
- Official case + built-in fan for cooling (not standalone Active Cooler inside the official case — can throttle).
- v1 camera = USB webcam (Logitech C270 class); v2 = AI Camera (IMX500).
- Train on Colab, never on the Pi (Pi too slow for training).
- Work from VS Code + Remote-SSH on the Mac; likely headless Pi.
- RTC battery skipped.
- Custom object: **not chosen yet.**

## Gotchas log
> Append dated notes when something breaks and how it got fixed.
- **Imager showed empty Storage list.** Card was in but Imager was opened first / needed re-scan. Fix: quit Imager fully (Cmd+Q), keep card in, reopen. (Confirm Mac sees card in Finder/Disk Utility first.)
- **`ping mypi.local` → "cannot resolve".** First boot takes a few minutes; `.local` can also be slow to resolve. Fix: wait, then find the Pi by IP (see triage commands in the guide) or via the AmpliFi app.
- **Chased the wrong IP — it was the Mac.** `arp -a` and a broadcast ping surfaced `192.168.166.178`, which turned out to be the Mac itself (`ipconfig getifaddr en0` confirmed). Lesson: always confirm an IP isn't your own Mac before SSHing.
- **Wrong username.** Tried `ssh oleg@...` but the flashed user was different at first. Fix: read the actual username from the card — `cat /Volumes/bootfs/user-data`. (Final working username: `oleg`.)
- **Wi-Fi network name must match exactly.** Confirmed the SSID in `cat /Volumes/bootfs/network-config` against the real network. Country was correctly set to `UA`.
- **Locale warnings on SSH login** (`LC_CTYPE`/`LC_ALL cannot change locale`). Harmless but noisy. Fix: generate the locale on the Pi — uncomment `en_US.UTF-8` in `/etc/locale.gen`, `sudo locale-gen`, `sudo update-locale`. (Quick-silence only: `sudo touch /var/lib/cloud/instance/locale-check.skip`.)
- **Fan connector hard to reach.** Plug the fan into the J17 FAN header *while the case lid is still open*, then close the lid — not after.
- **`git init` defaults to `master`, GitHub expects `main`.** Fix: `git branch -M main` before pushing.
- **GitHub rejects your account password on push.** Need a Personal Access Token (Settings → Developer settings → Personal access tokens → classic → `repo` scope); paste the token as the password.
- **VS Code extensions must be installed on the *remote* side.** With Remote-SSH, extensions that touch project files (e.g. Claude Code) show "Install in SSH: mypi.local" — click that, or they stay disabled in the workspace.
- **`pip install ultralytics` pulls dozens of `nvidia-*` CUDA packages.** The Pi has no NVIDIA GPU; they're unused PyTorch dependencies. Harmless, just disk space.
- **Careful which VS Code window is which.** One window was the Mac (`/Users/oleg/Desktop/cv-project`), the other the Pi (`SSH: mypi.local`). Work in the SSH one — check the green indicator bottom-left and that the terminal prompt reads `oleg@mypi`.
- **Headless = no display for `show=True`.** With no monitor on the Pi, YOLO can't open a preview window. Use `save=True` (writes annotated frames to `runs/detect/`) and print labels instead. A monitor on the Pi, or streaming the feed, is needed for a live window.
- **`Ctrl+C` during live detection prints a long traceback.** It's just the interrupt landing mid-inference — not a crash, expected behavior.
- **The C270 reports 30 FPS input**, but YOLO processes at ~3.4 FPS. The camera isn't the bottleneck — the Pi's CPU is.

---

## Notes for the next session
> Free-text scratchpad for "pick up here" reminders.
- **Blocked only on the webcam now.** Everything camera-independent is done: OS, network, VS Code, YOLO, still-image detection, project structure, Git + GitHub.
- **When the webcam arrives:** `sudo apt install -y fswebcam` → `fswebcam test.jpg` to confirm capture → create `detect_live.py` → `python detect_live.py` for live detection. Then record the demo GIF.
- **Can do right now without hardware:** decide the custom object; create free Roboflow + Google Colab accounts; start taking the 50–150 phone photos.
- **Remember:** activate the venv in every new terminal — `source ~/cv-project/venv/bin/activate` (prompt shows `(venv)`).
- **Docs sync:** the `.md` files are edited in chat and must be re-downloaded into `~/cv-project` on the Pi, then committed.
