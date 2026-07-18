from ultralytics import YOLO

model = YOLO("models/yolo11n.pt")

for r in model.predict(source=0, stream=True, save=True):
    print(r.verbose())
