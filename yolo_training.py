import os

# Solution rapide pour contourner le problème d'OpenMP
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from ultralytics import YOLO

# Charger le modèle YOLOv8m
model = YOLO(r'C:\Users\PC_DHIA\Desktop\tennisballprojectcv\models\yolov8m.pt')

# Effectuer le tracking sur la vidéo d'entrée en utilisant le CPU
results = model.track(source=r'C:\Users\PC_DHIA\Desktop\tennisballprojectcv\input_video\input_video.mp4',
                      conf=0.2, save=True, device='cpu')

# Optionnel: Afficher les résultats dans la console
print("***********===========>",results)
