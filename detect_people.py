from ultralytics import YOLO

model = YOLO("models/yolo11n.pt")

# classes=[0] restricts detection to a single COCO class: 0 = "person".
# The model still runs the same, but only reports people — everything
# else (cup, chair, laptop, ...) is ignored. This is the whole difference
# from detect_live.py.
#
# source=0    = the first camera (/dev/video0)
# stream=True = process frames one at a time as they arrive
# save=True   = write annotated frames to runs/detect/ (headless-friendly)
for r in model.predict(source=0, stream=True, save=True, classes=[0]):
    print(r.verbose())
