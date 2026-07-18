# Design Decisions & Rationale

> **Purpose of this file:** a record of the engineering decisions behind the project — the hardware, the workflow, and the AI stack — and *why* each choice was made. It complements the [`README.md`](./README.md) (how to build it) and the [`BUILD-LOG.md`](./BUILD-LOG.md) (what was done, in order, and the problems solved along the way).

---

## Project goal

Build a real-time computer-vision **object detector that runs entirely on a Raspberry Pi 5**, then extend it to recognize a custom object trained from scratch. All inference runs **on the device** ("edge AI") — no cloud round-trips — the same architecture as a smart camera such as Ring or Nest. The finished project is published as a portfolio piece with a reproducible, beginner-followable writeup.

## Hardware

| Decision | Rationale |
|---|---|
| **Raspberry Pi 5** (4GB or 8GB) | Enough CPU for usable on-device inference; also the target platform for the optional AI Camera (IMX500) upgrade. **16GB was rejected** — extra RAM does not speed up detection; the CPU is the bottleneck. |
| **Official case with built-in fan** | The Pi 5 runs hot under sustained inference and needs active cooling. Chosen over a standalone Active Cooler inside the official case, which can throttle. |
| **Official 27W USB-C power supply** | The Pi 5 requires a genuine 5V/5A supply; an underpowered charger causes brownouts and instability. |
| **32GB A2 microSD card** | Holds the OS; the A2 rating gives faster random I/O for OS use. Flashed from a laptop via a USB-C card reader. |
| **USB webcam (Logitech C270) for v1** | Plug-and-play, zero configuration — the simplest reliable camera for a first build. |
| **Raspberry Pi AI Camera (Sony IMX500) for v2** | Optional phase-2 upgrade that runs inference on the sensor itself, freeing the Pi's CPU. Targets the Pi 5 specifically. |

The RTC battery was skipped — not needed for this application.

## Development workflow

- **Edit on a laptop, run on the Pi.** Development is done in VS Code with the **Remote-SSH** extension; the editor runs on the laptop while all commands execute on the Pi. This is the standard, comfortable way to work with a headless Pi.
- **Headless setup.** No monitor or keyboard on the Pi. Hostname, user, Wi-Fi, and SSH are all configured in Raspberry Pi Imager *before first boot*, so the Pi joins the network and is reachable the moment it powers on.
- **Networking.** The Pi and laptop communicate over the home Wi-Fi network (SSH to the Pi's address). The only physical laptop↔Pi step is moving the microSD card across once during flashing.

## AI stack

| Layer | Choice | Rationale |
|---|---|---|
| **Model** | Ultralytics YOLO (`yolo11n` — nano) | Smallest, fastest YOLO variant; the right accuracy/speed trade for edge hardware. |
| **Runtime** | PyTorch on the Pi CPU, inside an isolated `venv` | Keeps the project's dependencies sealed off from the system Python that Raspberry Pi OS relies on. |
| **Labeling** | Roboflow (browser-based, free tier) | Beginner-friendly box drawing; exports directly to YOLO format. |
| **Training** | Google Colab (free cloud GPU) | Training is far heavier than inference — minutes on a cloud GPU versus days on the Pi. Train in the cloud, then copy the resulting `best.pt` to the device. |
| **Deployment** | Copy `best.pt` to the Pi, point the detection script at it | A single-line change swaps the custom model in for the pre-trained one. |

## Key tradeoffs

- **Modest frame rate is expected, not a bug.** A Pi 5 running all inference on a normal camera produces a modest frame rate (~3–3.4 FPS measured). This is the honest reality of edge hardware and is documented plainly rather than hidden.
- **A small, honest dataset is a legitimate result.** A custom model trained on ~60–150 phone photos detecting one object is a genuine, ship-worthy outcome. Ship v1, then improve.
- **Train in the cloud, run on the edge.** The deliberate split — heavy training off-device, lightweight inference on-device — is the core architectural idea and mirrors how production edge-AI systems are built.

## Roadmap

1. **v1 base** — USB webcam + `yolo11n` → live detection → phone alerting (Telegram) → publish to GitHub.
2. **Custom object** — collect photos → label in Roboflow → train on Colab → deploy `best.pt`.
3. **v2 (optional)** — port to the AI Camera (IMX500): export the model to IMX format and package it into a `.rpk` to run on-sensor. This is the most involved part; documenting the conversion clearly is high-value to other developers.
   - References: [Ultralytics IMX500 guide](https://docs.ultralytics.com/integrations/sony-imx500/) · [Raspberry Pi AI Camera docs](https://www.raspberrypi.com/documentation/accessories/ai-camera.html)

## Publishing goals

- A strong README with a demo GIF/video (highest-impact asset), a bill of materials, reproducible setup steps, and an honest "what I learned / tradeoffs" section.
- MIT license.
- Datasets are *described*, not committed — large image folders stay out of the repo.
