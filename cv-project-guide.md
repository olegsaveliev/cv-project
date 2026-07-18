# Raspberry Pi Object Detection — Beginner Project Guide

A hands-on computer vision project you can build with **no prior programming skills**, then publish to GitHub as a portfolio piece. You'll build a small device with a camera that detects objects in real time, then customize it to detect something of your choosing.

> **Who this is for:** Someone with conceptual AI understanding (like a former AI product manager) who wants real hands-on building experience. Every command is copy-paste. You don't need to understand the code to get it working — but you'll understand a lot more by the end.

---

## Part 0 — What you're building

A **Raspberry Pi 5** (a credit-card-sized computer) with a camera attached. It runs a pre-trained AI model called **YOLO** (You Only Look Once) that draws boxes around objects it sees and labels them — "person," "cup," "dog," etc. — live, on screen.

Once that works, you'll do the impressive part: **train it to detect a custom object you pick yourself.** That custom step is what makes your GitHub repo yours and not a copy of a tutorial.

**Why this project is a good showcase:**
- It's a real edge-AI device, not just a script — conceptually close to Ring/Nest-style products.
- The full pipeline (hardware → camera → model → custom training → deployment) is exactly what CV engineers actually do.
- It photographs and demos well, which matters for a portfolio.

### Simple camera vs. AI camera — where does the "thinking" happen?

This is the single most useful idea to understand, and it's simpler than it sounds.

**The detection has two jobs:**
1. **See** — capture the picture (all cameras do this).
2. **Think** — run the AI that finds objects in the picture and draws the boxes. *This is the heavy work.* Someone's processor has to do it.

The only question is: **whose processor does the thinking?**

**With a simple camera (USB webcam or Camera Module 3):**
The camera only *sees*. It sends the raw picture to the Raspberry Pi, and the **Pi's processor does all the thinking.** The Pi is a small computer, so it can only think so fast — that's why detection with a simple camera is usable but a bit slow (a modest frame rate). Think of the camera as an eye, and the Pi as the brain doing all the work.

**With the AI Camera (Sony IMX500):**
The camera *sees AND thinks.* It has a tiny AI chip built into the sensor, so it finds the objects **inside the camera itself** and sends the Pi just the answer ("cup, here; person, there") instead of a raw picture for the Pi to chew on. The Pi's processor stays free, and detection is fast and smooth. The eye now has a small brain of its own.

**What "edge" means (and why it matters):**
"The edge" just means *doing the AI right where the data is created* — on your device — instead of sending it off to a big server in the cloud. Both setups above are "edge AI" because the thinking happens on your desk, not in a data center. That's good for **privacy** (video never leaves your device), **speed** (no round-trip to the internet), and **cost** (no cloud bills). The AI Camera pushes this even further — Sony calls it "extreme edge" because the AI runs on the *sensor itself*, the furthest edge possible.

> **Analogy:** A simple camera + Pi is like a security guard (the Pi) watching a plain camera feed and identifying things himself. The AI Camera is like a smart camera that already knows what it's looking at and just radios the guard the summary. The second is faster and frees the guard up — but building your *own* custom "smart camera" takes an extra assembly step (that's the phase-2 complexity in Part 8).

This is exactly the architecture behind products like Ring/Nest doorbells, which is why it's a strong portfolio story for you.

---

## Part 1 — Shopping list (Ukraine)

The simplest route is a **Raspberry Pi 5 Starter Kit**, which bundles almost everything. Buy the kit + a camera, and you're done shopping.

### Recommended: buy a Starter Kit
Search Rozetka for **"Raspberry Pi 5 Starter Kit"**. The kit typically includes:
- Raspberry Pi 5 board (get the **4GB** version — plenty for this)
- Case with cooler/fan (the Pi 5 needs active cooling)
- microSD card (64GB)
- 27W USB-C power supply (the Pi 5 specifically needs a strong 5V/5A supply)
- micro-HDMI-to-HDMI cable

### Add separately: a camera
You have three options, in increasing order of "cool but complex":

1. **Any USB webcam** — simplest of all. Plugs into a USB port, works instantly, no ribbon cable. If you own one, start here.
2. **Raspberry Pi Camera Module 3** — the official ribbon-cable camera. Best plain image quality. *Note: the Pi 5 uses a narrower camera cable than older Pis — make sure the cable that comes with it fits the Pi 5, or buy the "Camera cable for Raspberry Pi 5" (part SC1129).*
3. **Raspberry Pi AI Camera (Sony IMX500)** — a camera with an AI accelerator *built into the sensor*. The neural network runs on the camera itself, not on the Pi's CPU, so live detection is much faster and smoother. More impressive and a stronger portfolio piece — but the custom-model path is more involved (see Part 8). Great as a **phase-2 upgrade**.

> **Beginner tip:** Start with a **USB webcam** if you have one, or Camera Module 3. Get the whole pipeline — including custom training — working the easy way first. Then, if you bought the AI Camera, "graduate" to it as phase 2. That v1→v2 progression is itself a great GitHub story: "v1 on webcam, v2 optimized for on-sensor inference."

> **Which camera should I buy?** If you want the smoothest first success and to focus your learning on training/labeling → Camera Module 3 or a USB webcam. If you want the more distinctive, faster, "real edge-AI product" result and don't mind more setup friction on the custom step → the AI Camera. A sensible move for someone learning deeply: **buy the AI Camera but keep a cheap USB webcam around for v1.**

#### Recommended v1 webcams (cheap, Linux-friendly, "just works")
For v1 you want a plain USB webcam. The Pi runs Linux, so look for a **UVC-compliant** camera (USB Video Class = plug in, works instantly, no drivers). Almost every mainstream USB webcam is UVC. You do **not** need 4K or autofocus — YOLO shrinks the image to about 640 pixels anyway, so 720p or 1080p is plenty. Sweet spot: a basic 1080p webcam, roughly 500–1,200 UAH.

- **Logitech C270** — the classic beginner pick. 720p, rock-solid Linux support, cheap, and the single most-tested webcam on Raspberry Pi. If you want zero surprises, buy this. *(Recommended.)*
- **Logitech C310 / C270 HD** — same family, a touch higher resolution, same reliability.
- **Logitech C920 / C922** — 1080p, excellent Linux support. Overkill for detection but a genuinely nice webcam for calls too. Costs more.
- **Trust / A4Tech / Sven basic 1080p webcams** — budget Ukrainian-market brands. Fine for v1 as long as the listing says USB + 720p/1080p. Slightly more of a quality lottery than Logitech.

**Search phrases to paste into Rozetka / MiniComp:** `Logitech C270`, or `веб-камера USB 1080p` (filter for USB, 720p/1080p). Any hit that's a plain USB webcam will work.

> **Cheapest path of all:** if you already own *any* USB webcam — even an old one in a drawer — use it for v1. It genuinely doesn't matter which; you're only proving the pipeline works. Save your money for the AI Camera (v2).

### Buying components separately (checklist)
If you're not buying a bundled kit, here's the full parts list so nothing is missed:

- **Raspberry Pi 5 board** — 4GB recommended (2GB works but is a bit tight for the VS Code + Claude Code workflow; 8GB only if you have other plans).
- **Power supply** — the official **27W USB-C** PSU. The Pi 5 needs a strong 5V/5A supply; don't reuse a random phone charger.
- **microSD card** — the official **32GB A2** card is an ideal pick (A2 = fast for running an OS).
- **Cooling + case** — pick **ONE**: the **official Pi 5 case with built-in fan** (simplest, cooling included — recommended), **OR** the standalone **Active Cooler** paired with an open/ventilated "Active Cooler-compatible" case. Do **not** put the standalone Active Cooler inside the official case — that combo can actually throttle.
- **micro-HDMI-to-HDMI cable** — needed only if you'll use a monitor for setup. (A cable "for Pi 4" is fine — the port is identical.) Skip if going fully headless.
- **USB-C microSD card reader** — for flashing the card from your MacBook Air (no card slot on the Air).
- **Camera** — v1: a USB webcam (Logitech C270). v2 (optional later): the AI Camera (IMX500).
- **Skip:** the RTC battery — not needed.

### Where to buy in Ukraine
- **minicomp.com.ua** — specializes in Raspberry Pi, Ukraine-wide delivery, sells the AI Camera.
- **rozetka.com.ua** — biggest selection, multiple sellers.
- **arduino.ua** — maker/DIY focused, good for camera modules.
- **electronoff.ua** — electronics components.

### You'll also need (probably already own)
- A monitor with HDMI + a USB keyboard/mouse (for setup only — **not needed if going headless**).
- Your **MacBook Air M4** to flash the microSD card and to run VS Code.
- Wi-Fi (built into the Pi) — have your network name and password handy.

### Rough budget note
Buying separately, a 4GB board + PSU + card + case-with-fan + a USB webcam is a reasonable outlay; the exact total depends on the shop. A bundled Starter Kit (e.g. ~9,860 UAH for 4GB at MiniComp) can be cheaper than separate parts — worth comparing before you commit. The 16GB kit is overkill; extra RAM does not speed up detection.

---

## Part 2 — First-time Pi setup

### Step 2.1 — Flash the operating system (from your MacBook)

You put the OS onto the **microSD card** (not an SSD — the Pi boots from the microSD card). On a MacBook Air you'll need a **USB-C microSD card reader**, since the Air has no card slot.

> **Note on terminology:** the storage here is a *microSD card*, not an SSD. The Pi 5 boots from the microSD card slot on the underside of the board.

1. **Install Raspberry Pi Imager** on your Mac from `raspberrypi.com/software`. Install it like any Mac app.
2. **Insert the microSD card** into your USB-C card reader, and plug the reader into the MacBook.
3. **Open Raspberry Pi Imager.** Click the three buttons in turn:
   - **Choose Device** → **Raspberry Pi 5**
   - **Choose OS** → **Raspberry Pi OS (64-bit)** (recommended, at the top)
   - **Choose Storage** → your **microSD card** (double-check you pick the card, not another drive)
4. Click **Next** → when asked to **edit settings**, choose **Edit Settings**. This step is what makes the MacBook-controlled (headless) workflow work — don't skip it. Set:
   - **Hostname** (e.g. `mypi`)
   - **Username + password** (write these down — you'll need them to connect from VS Code)
   - **Wi-Fi name + password** (so the Pi auto-joins your network on first boot)
   - **Locale / timezone**
   - Then the **Services** tab → **enable SSH** → "use password authentication"
5. **Save**, then **Write**. It erases the card, writes the OS, and verifies. Takes a few minutes; it may ask for your Mac password — normal.
6. When done, **eject** the card, remove it from the reader, and insert it into the **Pi's microSD slot** (underside of the board).

> **Why set Wi-Fi + SSH now?** Because then the Pi joins your network and is reachable from your Mac the instant it powers on — no monitor or keyboard needed. Your card may ship pre-loaded with Raspberry Pi OS, but flash it yourself anyway so your Wi-Fi and SSH settings are baked in.

### Step 2.2 — First boot
1. Insert the flashed microSD card, connect the camera, then plug in power. (Headless route: no monitor/keyboard needed — it joins Wi-Fi automatically. With-monitor route: also connect monitor/keyboard/mouse.)
2. Give it a minute to boot and join Wi-Fi. If using a monitor, it boots to a desktop; go through the welcome setup.

### Step 2.3 — Open a terminal
Everything from here is typed into the **Terminal** app (black icon in the top bar). Don't be intimidated — you're just pasting commands. Update the system first:

```bash
sudo apt update && sudo apt full-upgrade -y
```

Type your password when asked (it won't show characters — that's normal). Let it finish, then reboot:

```bash
sudo reboot
```

---

## Part 2.5 — Work from VS Code on your Mac (recommended)

Instead of typing commands on the Pi's tiny screen, you'll edit and run everything from **VS Code on your MacBook**, while it actually executes on the Pi. This is the standard professional Raspberry Pi workflow and it removes almost all the friction. Combined with headless operation, the Pi can sit in a corner with just power + camera, and you drive it entirely from your Mac.

### Step 2.5.1 — One-time prep on the Pi
SSH must be enabled. If you ticked "enable SSH" in Raspberry Pi Imager, it already is. Otherwise, on the Pi run:

```bash
sudo raspi-config
# Interface Options → SSH → Enable
```

Find the Pi's address (you'll need it to connect):

```bash
hostname -I     # shows the Pi's IP address, e.g. 192.168.1.42
hostname        # shows the Pi's name, e.g. mypi
```

### Step 2.5.2 — On your MacBook
1. Install **VS Code** (`code.visualstudio.com`).
2. In VS Code, open the Extensions panel and install **Remote - SSH** (by Microsoft).
3. Press `Cmd+Shift+P`, type **"Remote-SSH: Connect to Host"**, choose **Add New SSH Host**, and enter:
   ```
   ssh yourusername@192.168.1.42
   ```
   (use the username you set in Imager and the IP from above)
4. Connect. Enter the Pi's password when asked. VS Code opens a window that *is* the Pi — its files, its terminal, all on your Mac's screen.

> **Tip:** To avoid typing the password every time, you can set up an SSH key later — ask Claude Code to walk you through `ssh-keygen` and `ssh-copy-id`. Not required to start.

### Step 2.5.3 — Open your project
Once connected, `File → Open Folder → /home/yourusername/cv-project` (you'll create this in Part 4). The built-in terminal (`Ctrl+` `` ` ``) runs commands *on the Pi*. From here, everything in Parts 4–8 can be done inside VS Code.

### Step 2.5.4 — Claude Code (optional but recommended)
Install the **Claude Code** extension to have an AI assistant in the editor. It runs on your Mac and can read/edit the Pi's files through the Remote-SSH connection. It's ideal for explaining errors in plain English, writing/fixing the detection scripts, and walking through the fiddly IMX500 conversion in Part 8.

> **Learning tip:** lean on it to *explain*, not just to *do*. Ask "why does this line exist?" and "what does this error mean?" — since your goal is hands-on learning, that's the difference between a repo you understand and one you can only copy. Hand it the `DESIGN.md` file (see below) at the start of a session so it knows your setup and decisions without you re-explaining.

### Step 2.5.5 — Finding the Pi & fixing first-boot problems (real triage)
The most common snags are all at first connection. These are the exact commands to diagnose them — run them **on your Mac** unless noted. This is a genuinely useful reference; first-boot networking trips up almost everyone.

**1. Try to reach the Pi by name:**
```bash
ping -c 3 mypi.local        # replace "mypi" with your hostname
```
- Replies with an IP (e.g. `192.168.x.x`) → good, note that IP.
- "cannot resolve" → the Pi may still be booting (wait 3–5 min) or `.local` isn't resolving; find it by IP below.

**2. Find the Pi by IP when the name fails:**
```bash
ping -c 1 192.168.X.255     # your network's broadcast address; wakes up the device list
arp -a                      # lists devices on the network
```
Look for an unfamiliar `192.168.X.x` line — a candidate for the Pi. (Your router range: check `ping mypi.local` once it works, or your router app.)

**3. Make sure a candidate IP isn't your own Mac** (easy mistake — a machine pinging itself replies in ~0.7ms):
```bash
ipconfig getifaddr en0      # prints YOUR Mac's IP. If a candidate matches this, it's the Mac, not the Pi.
```

**4. Best tool of all — your router's device list.** Open your router's app/admin page (e.g. AmpliFi app) and look for a device named `mypi` or `raspberrypi`; it shows the exact IP.

**5. If the Pi never appears on the network**, the Wi-Fi settings probably didn't take. You can *read what was actually written to the card* — put the card back in your Mac and:
```bash
cat /Volumes/bootfs/network-config   # shows the Wi-Fi SSID + country that got saved
cat /Volumes/bootfs/user-data        # shows the hostname + USERNAME that got saved
```
Check the **SSID matches your network exactly**, a **country code** is present (e.g. `UA`), and note the **real username** (it's easy to misremember — connect with `ssh THATUSERNAME@mypi.local`). If wrong, re-flash in Imager with corrected Wi-Fi.

**6. Connect once reachable:**
```bash
ssh yourusername@mypi.local        # or ssh yourusername@192.168.X.x
```
First time asks to confirm the fingerprint → type `yes`. Then the Pi password (nothing shows as you type — normal). Prompt changes to `yourusername@mypi:~ $` = you're in.

**7. Silence the locale warnings** that often appear on first SSH login (`LC_CTYPE`/`LC_ALL: cannot change locale`). Harmless, but to fix properly, **on the Pi**:
```bash
sudo sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
sudo locale-gen
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
```
Then log out (`exit`) and SSH back in.

---

## Part 3 — Get the camera working

### If using a USB webcam
Plug it in. Test it:

```bash
sudo apt install -y fswebcam
fswebcam test.jpg
```

Open `test.jpg` from the file manager. If you see an image, you're good.

### If using the Raspberry Pi ribbon camera
Test with the built-in tool:

```bash
rpicam-hello --timeout 5000
```

A preview window should appear for 5 seconds. If it doesn't, re-seat the ribbon cable (blue side facing the correct way — check the Pi's camera port orientation) and make sure it clicked into the slot.

---

## Part 4 — Install the AI (YOLO)

We'll use **Ultralytics YOLO**, the most beginner-friendly modern detection library. These commands set up an isolated Python environment (good practice) and install it.

```bash
# Create a project folder
mkdir ~/cv-project && cd ~/cv-project

# Create an isolated Python environment
python3 -m venv venv
source venv/bin/activate

# Install YOLO
pip install ultralytics
```

That last install takes several minutes on a Pi. Grab a coffee.

> **What just happened:** You installed a library that includes pre-trained models able to recognize 80 common object types out of the box (people, cars, animals, bottles, laptops, etc.). This is the "detect whatever" starting point.

---

## Part 5 — Run your first detection

### Test on a single image
Still inside the `venv` (you'll see `(venv)` at the start of your terminal line):

```bash
yolo predict model=yolo11n.pt source=test.jpg
```

The first run downloads the model automatically. When done, it saves an annotated image (with boxes + labels) into a `runs/detect/` subfolder. Open it — you've done object detection!

### Run it live on the camera
Create a small script. Type this to open a text editor:

```bash
nano detect_live.py
```

Paste this in:

```python
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

# source=0 is the first camera (USB webcam or Pi camera)
model.predict(source=0, show=True, stream=True)

# Keep the window open by consuming the stream
for _ in model.predict(source=0, show=True, stream=True):
    pass
```

Save and exit nano: press `Ctrl+O`, then `Enter`, then `Ctrl+X`.

Run it:

```bash
python detect_live.py
```

A window opens showing your camera feed with live boxes and labels. **This is the core of your project working.** Wave a cup or your phone in front of it.

> **Performance note:** A Pi 5 runs the small "nano" model at a usable but modest frame rate. That's expected for edge hardware and is a good thing to mention honestly in your GitHub README — it's a real engineering tradeoff, not a flaw.

---

## Part 6 — The showcase step: detect YOUR custom object

This is what turns a tutorial into a portfolio project. You'll teach the model one new thing it didn't know before. You don't need to decide *what* until now — good candidates are objects that are: distinct-looking, easy for you to photograph 50–150 times, and tell a small story.

**Ideas:** your specific coffee mug, a particular tool, a plant's health state (healthy vs. wilting leaf), whether your mailbox flag is up, a specific product/package type, hard-hat-on vs. hard-hat-off (a classic safety-CV demo).

### The workflow (high level)
1. **Collect images** of your object — 50 to 150 photos, varied angles/lighting/backgrounds. Your phone is fine.
2. **Label them** — draw boxes around your object in each image and tag them. Use a free tool:
   - **Roboflow** (`roboflow.com`) — browser-based, beginner-friendly, has a generous free tier, and can export directly in YOLO format. Strongly recommended for a first custom model.
   - Or **Label Studio** / **CVAT** if you prefer self-hosted.
3. **Train** — feed the labeled images to YOLO. On a Pi this is slow; instead do the training step on **Google Colab** (free cloud GPUs in your browser) — Roboflow provides ready-made Colab notebooks where you mostly just press "Run."
4. **Deploy** — download the resulting trained model file (`best.pt`), copy it to the Pi, and point your `detect_live.py` at it instead of `yolo11n.pt`.

### The one line that changes
After training, in your script:

```python
model = YOLO("best.pt")   # your custom model instead of yolo11n.pt
```

Everything else stays the same — now it detects your object.

> **Don't over-engineer the first version.** A model trained on 60 phone photos that detects one object at 80% accuracy is a *completely valid* portfolio project. Ship it, then improve. "Working and honest" beats "ambitious and unfinished" every time on GitHub.

---

## Part 7 — Publish to GitHub

### What makes a good repo
Recruiters and peers skim the **README** first. A strong README has:
- **A GIF or short video** of the detector working (record your screen — this is the single highest-impact thing you can add).
- **What it does**, in two sentences.
- **Hardware used** (Pi 5, camera model) — bill of materials.
- **Setup instructions** (you basically already wrote them above).
- **What you learned / tradeoffs** — a short honest section. Mention the frame-rate reality, why you trained in the cloud, what you'd improve. This maturity reads very well.
- **Credit** to Ultralytics YOLO and Roboflow.

### Suggested repo structure
```
my-cv-detector/
├── README.md
├── detect_live.py
├── requirements.txt        # just: ultralytics
├── models/
│   └── best.pt             # your trained model
├── docs/
│   └── demo.gif
└── data/
    └── README.md           # describe your dataset (don't commit huge image folders)
```

### Getting it up (from the Pi or laptop)
```bash
cd ~/cv-project
git init
git add .
git commit -m "Custom object detector on Raspberry Pi 5"
# create an empty repo on github.com first, then:
git remote add origin https://github.com/YOURNAME/my-cv-detector.git
git branch -M main
git push -u origin main
```

> **License tip:** Add an MIT license (GitHub offers it in one click when creating the repo) so others can freely learn from your work.

---

## Part 8 — Phase 2 (optional): the AI Camera (Sony IMX500)

This is the "graduate" step if you bought the **Raspberry Pi AI Camera**. It's genuinely more impressive — the neural network runs *on the camera sensor itself*, so the Pi's CPU stays free and detection is fast and smooth. It's the same architecture Sony demos publicly with YOLO, and conceptually it's exactly the "AI on the device" edge design. Fewer beginners have done it, so it stands out on GitHub.

**Read this before deciding to do phase 2:** the tradeoff is that your custom model can't just be dropped in as a `best.pt` file. It has to be *converted and compiled* into the sensor's special format (called IMX500, file extension `.rpk`) using Sony's toolchain. That conversion is the one genuinely fiddly part of this whole project. Out-of-the-box detection (the 80 common objects) is easy on the AI Camera; the custom step is where the extra patience goes.

### Step 8.1 — Connect the camera and install the firmware/tools
Attach the AI Camera to the Pi 5's camera port (same as any ribbon camera — mind the Pi 5 cable). Then install the IMX500 firmware and tools:

```bash
sudo apt update
sudo apt install -y imx500-all imx500-tools
sudo apt install -y python3-picamera2 rpicam-apps git python3-venv python3-pip
```

The first time the camera runs, it downloads firmware onto the sensor — this is normal and takes a moment.

### Step 8.2 — Run the ready-made detection demo (the easy win)
Raspberry Pi ships pre-packaged models, so you can see on-sensor detection working immediately without training anything:

```bash
# Get the example scripts
git clone https://github.com/raspberrypi/picamera2.git
cd picamera2/examples/imx500

# Run object detection with a pre-packaged YOLO model
python imx500_object_detection_demo.py \
  --model /usr/share/imx500-models/imx500_network_yolo11n_pp.rpk \
  --bbox-normalization --bbox-order xy --threshold 0.15
```

If boxes appear on the camera feed, the whole on-sensor pipeline works. This alone is a legitimate demo to record.

### Step 8.3 — The custom-model workflow (the involved part)
This replaces the simple "swap in best.pt" step from Part 6. The flow is:

1. **Collect and label images** — exactly as in Part 6 (Roboflow works fine).
2. **Train your YOLO model** — same as Part 6, on Google Colab. You end up with a trained model.
3. **Export to IMX500 format** — instead of stopping at `best.pt`, you run Ultralytics' IMX export, which quantizes the model and produces sensor-ready files:

   ```python
   from ultralytics import YOLO
   model = YOLO("best.pt")           # your trained model
   model.export(format="imx", data="your_dataset.yaml")
   ```

   This step needs care: quantization can slightly change accuracy, and the export has specific dependencies. Do this on your laptop/Colab, not the Pi.

4. **Package into a `.rpk` file** — on the Pi, compile the exported model into the sensor's loadable format:

   ```bash
   imx500-package -i packerOut.zip -o out
   # produces out/network.rpk
   ```

5. **Run your custom `.rpk`** — point the same demo script at your file instead of the pre-packaged one:

   ```bash
   python imx500_object_detection_demo.py \
     --model out/network.rpk \
     --labels labels.txt \
     --bbox-normalization --bbox-order xy --threshold 0.15
   ```

### If phase 2 fights you
This is the part where beginners hit snags, and that's expected — pushing through it is real edge-AI engineering experience. Two reliable references that walk the exact IMX500 export path with working commands:
- **Ultralytics IMX500 guide:** `docs.ultralytics.com/integrations/sony-imx500`
- **Raspberry Pi AI Camera docs:** `raspberrypi.com/documentation/accessories/ai-camera.html`

Common gotchas: `imx500-package: command not found` → `sudo apt install -y imx500-tools`; camera not found → `rpicam-hello --list-cameras` and set the camera index accordingly.

> **GitHub angle:** documenting the IMX500 conversion clearly — the thing that tripped you up and how you fixed it — is often *more* valuable to other developers than the detector itself. Write that part up honestly and it becomes the most-read section of your repo.

---

## Suggested learning arc (no rush)

Since you want to learn deeply, here's a sensible order rather than doing it all at once:

1. **Weekend 1:** Buy the kit. Flash OS, boot, get camera working. *(Parts 1–3)*
2. **Weekend 2:** Install YOLO, run detection on images and live camera. Play with it. *(Parts 4–5)*
3. **Week 3–4:** Pick your custom object. Collect and label images. Train on Colab. *(Part 6)*
4. **Week 5:** Polish, record a demo GIF, write the README, publish **v1**. *(Part 7)*
5. **Phase 2 (optional, weeks after):** if you have the AI Camera, port to on-sensor inference and publish **v2**. *(Part 8)* This is where the project goes from "solid" to "distinctive."
6. **Later, optional depth:** try a bigger YOLO model and compare speed/accuracy; add a simple alert (e.g., notify when your object appears); read the Ultralytics docs to understand confidence thresholds and what the numbers mean.

---

## If you get stuck

- **Ultralytics docs:** `docs.ultralytics.com` — genuinely beginner-readable.
- **Roboflow learn:** step-by-step custom training guides with videos.
- **Raspberry Pi docs:** `raspberrypi.com/documentation` for anything hardware/OS.
- When an error appears, copy the **last few lines** of it — that's the actual message — and search it, or paste it to an AI assistant for a plain-English explanation.

You've got the conceptual background already. The only new muscle here is getting comfortable pasting commands and not panicking at red error text — everyone hits errors, resolving them *is* the hands-on experience you're after.
