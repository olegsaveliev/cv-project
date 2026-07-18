# PROJECT-CONTEXT.md

> **Purpose of this file:** the *general approach* — who I am, the decisions already made, and how to help — so Claude Code doesn't start from scratch each session. This is the "how we think about the project" file.
>
> **File map:** [`CLAUDE.md`](./CLAUDE.md) is the short entry point → this file is the approach/decisions → [`MEMORY.md`](./MEMORY.md) is live status against the plan (**update it as we go**) → [`cv-project-guide.md`](./cv-project-guide.md) is the full build guide → [`README.md`](./README.md) is the public GitHub writeup. **Live status lives in MEMORY.md, not here.**

---

## Who I am / how to help me
- I'm a former AI product manager (worked on AI at Amazon Ring). I understand AI concepts well but have **limited hands-on coding experience**.
- My goal is **hands-on learning**, not just a finished product. When you write code or fix errors, **explain what you did and why**, in plain terms. I'd rather understand 5 lines than blindly paste 50.
- Please **explain errors in plain English** and teach me the debugging reasoning, not just the fix.
- Location: Kyiv, Ukraine.

## The project
Build a real-time computer vision **object detector** on a **Raspberry Pi 5**, then customize it to detect a custom object of my choosing, and **publish it to GitHub** as a portfolio piece. It's an edge-AI device — conceptually similar to Ring/Nest — which ties to my background.

## Hardware (decided)
- **Raspberry Pi 5** — buying **components separately** (not a bundled kit). Board: 4GB is the target (2GB works but is tight for the VS Code + Claude Code workflow; 8GB only if other plans arise).
- **Power supply:** official 27W USB-C (Pi 5 needs 5V/5A — not a random phone charger).
- **microSD card:** official 32GB A2 card (A2 = fast for OS use). Flashed from the MacBook.
- **Cooling/case:** the **official Pi 5 case with built-in fan** (cooling included, simplest — chosen). NOT the standalone Active Cooler inside the official case (that combo can throttle). Standalone Active Cooler only makes sense with an open/vented case built for it.
- **micro-HDMI→HDMI cable:** only if using a monitor for setup (a "for Pi 4" cable is fine). May skip if fully headless.
- **USB-C microSD card reader:** needed to flash the card from the MacBook Air (no card slot).
- **v1 camera:** a plain **USB webcam** (Logitech C270 or similar). Easiest, plug-and-play.
- **v2 camera (optional, later):** **Raspberry Pi AI Camera (Sony IMX500)** — runs inference on the sensor itself. Phase-2 upgrade. (Note: AI Camera targets the Pi 5, another reason to stay on Pi 5 not Pi 4.)
- My personal computer is a **MacBook Air M4 (24GB/500GB)**. I work from it.
- Peripherals I own: Logitech MX Master mouse + MX Keys Mini keyboard (Bluetooth/Logi Bolt). Monitor available. Will buy any missing setup bits.
- Bought in Ukraine (minicomp.com.ua / rozetka.com.ua).

## Workflow (decided)
- I work from **VS Code on my MacBook**, connected to the Pi via the **Remote - SSH** extension. Commands run on the Pi; I edit on the Mac.
- Prefer this remote workflow over typing on the Pi directly. Leaning toward **headless** setup (no monitor/keyboard on the Pi).
- **Flashing:** OS goes on the **microSD card** (not an SSD) using **Raspberry Pi Imager on the Mac**, via a USB-C card reader. In Imager's "Edit Settings" I set hostname, username/password, Wi-Fi, and enable SSH BEFORE first boot — this is what makes headless + VS Code work.
- **Pi ↔ Mac connection:** they talk over the **home Wi-Fi network** (SSH to the Pi's IP), NOT via a cable between them. The only physical Mac↔Pi moment is moving the microSD card across once. Ethernet to the router is an optional fallback if Wi-Fi is flaky.
- SSH is enabled on the Pi (set during flashing).

## The AI stack (decided)
- **Ultralytics YOLO** (model `yolo11n.pt` to start — the small/nano model, appropriate for Pi).
- Isolated Python virtual environment (`venv`) in `~/cv-project`.
- **Labeling:** Roboflow (browser-based, free tier, exports YOLO format).
- **Training:** Google Colab (free cloud GPU) — do NOT train on the Pi, it's too slow. Train in the cloud, then copy the resulting `best.pt` to the Pi.
- **Deployment:** copy trained `best.pt` to the Pi, point the detection script at it.

## Plan / phases
- **v1:** USB webcam + `yolo11n.pt` → live detection working → train ONE custom object via Roboflow+Colab → drop in `best.pt` → publish to GitHub.
- **v2 (optional):** port to the AI Camera (IMX500). This requires exporting the model to IMX500 format (`model.export(format="imx", ...)`) and packaging it into a `.rpk` file with `imx500-package`. This is the fiddliest part — expect to spend time here. Refs: docs.ultralytics.com/integrations/sony-imx500 and raspberrypi.com/documentation/accessories/ai-camera.html

## Key facts / decisions to remember
- 16GB Pi was rejected as overkill — extra RAM does NOT speed up detection; the CPU/GPU is the bottleneck.
- RTC battery: skipped, not needed.
- Pi 5 modest frame rate on a normal camera is EXPECTED (a real edge tradeoff) — mention it honestly in the README, it's not a bug.
- A custom model trained on ~60–150 phone photos detecting one object is a legitimate, ship-worthy portfolio result. Ship v1, then improve.
- **What object to detect: NOT DECIDED YET.** (Update this line once I choose.)

## GitHub goals
- Strong README with a demo GIF/video (highest-impact item), bill of materials, setup steps, and an honest "what I learned / tradeoffs" section.
- MIT license.
- Don't commit huge image folders; describe the dataset instead.
- If doing v2, documenting the IMX500 conversion clearly is high-value to other developers.

## Current status
**Live status lives in [`MEMORY.md`](./MEMORY.md)** — check there for where we are and the next step. Keep it as the single source of truth; don't duplicate the checklist here.

## How to start a session
When I open a new Claude Code session, I'll point you at [`CLAUDE.md`](./CLAUDE.md). Please:
1. Read this file (approach/decisions) and [`MEMORY.md`](./MEMORY.md) (current status).
2. Tell me where we are and confirm the next step.
3. Help with that step, explaining as you go.
4. At the end, **update [`MEMORY.md`](./MEMORY.md)** — tick off what got done, log any decisions/gotchas, set the next step.
