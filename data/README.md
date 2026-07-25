# Dataset

> The raw images are **not committed** (kept out of the repo). This file describes the dataset instead.

## Funko Pop detector (custom object, Phase 5)

A single-class object-detection dataset for the label **`funko_pop`** — detect any Funko Pop, regardless of character.

| | v1 | v2 (current) |
|---|---|---|
| Funko photos (positives) | 51 | 81 (51 + 30 more varied) |
| Negative / background images | 0 | 20 |
| Classes | 2 *(a stray `funko-pop-detector` slipped in)* | 1 (`funko_pop`) |
| Result (validation) | ~0.98 mAP50, but **false-fired live** | **mAP50 0.995**, mAP50-95 0.921 |

**How it was collected & prepared**
- Phone photos of a personal Funko collection, varied by angle, distance, lighting, and background.
- **v2 negatives** (the key fix): photos of people, legs, rooms, and clutter with **no Funko**, marked as null/background — added after v1 over-fit and started boxing legs as Funkos.
- Labelled and split in **Roboflow** (70 / 20 / 10 train / valid / test), with augmentations (rotation, brightness, blur).
- Trained on **Google Colab** (free T4 GPU): `yolo11n.pt`, 100 epochs, `imgsz=640`, ~8 minutes.

**Key lesson:** the jump from v1 to v2 wasn't more Funko photos — it was adding *negatives* so the model learned the object instead of a "tall thing in frame" shortcut. See [`FunkoPop/README.md`](../FunkoPop/README.md) for the full manual.

**Deliverable:** the trained weights `best.pt` → `../models/best.pt` (also gitignored; too large to commit casually).
