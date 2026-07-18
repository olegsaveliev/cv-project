# CLAUDE.md

> **Read me first.** This is the entry point for any Claude Code session on this project. It's deliberately short: it tells you what the project is and points you to the files that hold the detail. Read the linked files before suggesting or building anything.

## What this project is
A real-time computer vision **object detector** on a **Raspberry Pi 5**, later customized to detect one object of the owner's choosing, then **published to GitHub** as a portfolio piece. It's an edge-AI device — the AI runs on the device, not in the cloud — conceptually similar to a Ring/Nest camera. The owner is a former AI product manager (ex–Amazon Ring) who understands AI concepts but has limited hands-on coding experience, and whose main goal is **learning by doing**.

## How to help (the short version)
- Explain what you do and why, in plain terms. Teach the reasoning, especially for errors. Prefer the owner understanding 5 lines over pasting 50.
- Work step by step against the plan. Confirm which step we're on before diving in.
- Keep `MEMORY.md` up to date as work progresses (see below).
- **Keep `README.md` in sync with reality.** Whenever development changes something a beginner following the README would need — a command, a step, the hardware, a version, the order of operations, or a workaround for a problem we hit — update `README.md` in the same session so it always matches how the project actually works. The README is a living document, not a one-time writeup.

## The files (read in this order)
1. **[PROJECT-CONTEXT.md](./PROJECT-CONTEXT.md)** — the *general approach*: who the owner is, all hardware/software decisions already made, the workflow, the AI stack, and the phase plan. This is the "how we think about the project" file. Start here.
2. **[MEMORY.md](./MEMORY.md)** — the *live status tracker*. Where we are against the plan, what's done, what's next, and a running log of decisions and gotchas. **Update this file as we go** — it's the project's memory across sessions.
3. **[cv-project-guide.md](./cv-project-guide.md)** — the *full build guide*: every step from shopping to first AI detection to phase-2 AI Camera, with all commands. The reference manual.
4. **[README.md](./README.md)** — the *public GitHub README*: a polished, beginner-followable writeup of the whole journey. This is the deliverable others will read. Keep it accurate as the build evolves.

## Folder structure & where these files live
Everything lives in one project folder on the Pi: **`~/cv-project/`** (opened in VS Code over Remote-SSH). This same folder becomes the GitHub repo at publish time. Keep it organized like this, and create the sub-folders as each phase reaches them — don't make them all up front:

```
cv-project/
├── CLAUDE.md              # this file — entry point for AI sessions
├── PROJECT-CONTEXT.md     # approach & decisions
├── MEMORY.md              # live status (keep updated)
├── cv-project-guide.md    # full build guide (reference)
├── README.md             # public GitHub writeup (keep in sync)
├── LICENSE               # MIT (added at publish time)
├── requirements.txt      # python deps — just: ultralytics
├── detect_live.py        # the live detection script (created in Step/Part on detection)
├── models/               # trained model files
│   └── best.pt           # custom model (after training) — don't commit huge files casually
├── docs/                 # things for the README
│   └── demo.gif          # screen recording of it working (highest-impact asset)
└── data/                 # dataset info
    └── README.md         # DESCRIBE the dataset here; do NOT commit big image folders
```

**Rules for keeping it tidy:**
- All five `.md` files sit at the **root** of `cv-project/`. Don't move or rename them — the links between them are relative.
- The `venv/` virtual environment also lives in this folder but must **not** be committed to GitHub — add it to `.gitignore` (along with `runs/`, large images, and `*.pt` if they get big).
- Create `models/`, `docs/`, `data/` only when the phase that needs them arrives (training, demo recording, dataset). Note their purpose in `MEMORY.md` when you do.
- When you add a new file or folder that a beginner following the README should know about, reflect it in `README.md`'s structure section too.

## At the start of every session
1. Read `PROJECT-CONTEXT.md` and `MEMORY.md`.
2. Tell the owner where we are (from `MEMORY.md`) and what the next step is.
3. Help with that step, explaining as you go.
4. **Before ending:**
   - Update `MEMORY.md` — tick off what got done, note any decisions or gotchas, set the next step.
   - If anything changed how the project is built or run, update `README.md` too so it stays accurate for a beginner following it.

## How the project unfolds
The build is phased — the folder above fills in as you go, it isn't all created at once. Full detail is in `cv-project-guide.md`; the arc is:

1. **Hardware & OS** — order parts, flash Raspberry Pi OS to the microSD from the Mac (Wi-Fi + SSH set in Imager), first boot, update. *Folder: just the `.md` files so far.*
2. **Remote workflow** — connect VS Code (Remote-SSH) from the Mac to the Pi; create/open `~/cv-project`. *This is when the `.md` files land in the folder.*
3. **Camera** — confirm the camera captures an image before adding AI.
4. **Generic detection (v1 base)** — create `venv`, install `ultralytics`, run detection on an image, then live via `detect_live.py`. *Adds `detect_live.py`, `requirements.txt`, `venv/`.*
5. **Custom object (the showcase)** — collect photos → label in Roboflow → train on Colab → get `best.pt` → point the script at it. *Adds `models/best.pt`, `data/`.*
6. **Publish v1** — polish `README.md`, record `docs/demo.gif`, add `LICENSE`, push to GitHub. *Folder becomes the repo.*
7. **v2 (optional)** — port to the AI Camera (IMX500): export to `.rpk`, run on-sensor. *Adds IMX500 artifacts + README section.*

Match work to the current phase in `MEMORY.md`; create sub-folders only when their phase arrives.
