from ultralytics import YOLO

model=YOLO('models/best.pt')

results=model.predict('input_videos/input.mp4', save=True)

print(results[0])

for box in results[0].boxes:
  print(box)