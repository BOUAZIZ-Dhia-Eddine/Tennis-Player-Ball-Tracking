# 🎾 Tennis Player & Ball Tracking with Computer Vision  

This project focuses on **tracking tennis players and the ball** in real-time from match videos, replicating the professional broadcast analysis used in tournaments.  

Using a combination of **YOLOv5/YOLOv8, ResNet, and Kalman Filter**, the system detects and tracks players and the ball, analyzes their movements, and overlays traces/paths on the video for deeper performance insights.  

👉 [🎥 Demo on LinkedIn](https://www.linkedin.com/posts/bouaziz-dhia-eddine_computervision-spyder-yolo-activity-7241618441156083712-jz6M?utm_source=share&utm_medium=member_desktop&rcm=ACoAAECSnecBdpjNvFsR34dZ_OWJ-PWWrRUj5F0)  
👉 [⬇️ Download Demo Video](outputvideos/output_video20.avi)  

---

## 🚀 Features  

- **Player Detection & Tracking**  
  - Detects players using **YOLOv5 / YOLOv8** models.  
  - Robust to camera movement and partial occlusions.  

- **Ball Detection & Tracking**  
  - Uses **YOLO** models for ball detection.  
  - **Kalman Filter** applied to handle missed detections, motion blur, or false positives.  

- **Trajectory Analysis**  
  - Tracks ball trajectories during rallies.  
  - Computes player movement paths across the court.  

- **Overlay Visualization**  
  - Draws movement traces of players and the ball on top of the video frames.  
  - Similar to professional sports analytics.  

---

## 🛠️ Tech Stack  

- **Deep Learning Models**:  
  - [YOLOv5](https://github.com/ultralytics/yolov5) / [YOLOv8](https://github.com/ultralytics/ultralytics) for real-time detection.  
  - [ResNet](https://arxiv.org/abs/1512.03385) for feature extraction and improving classification robustness.  

- **Tracking**:  
  - **Kalman Filter** for smoothing trajectories and handling missing detections.  

- **Programming Language**: Python 🐍  
- **Frameworks/Libraries**: OpenCV, NumPy, PyTorch  

---

## 📂 Project Structure  

