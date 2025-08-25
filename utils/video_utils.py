# -*- coding: utf-8 -*-
import cv2 
import os

def read_video(path_video):
    if path_video:
        cap = cv2.VideoCapture(path_video)
        if not cap.isOpened():
            print("Problem opening video")
            return []

        liste_frames = []
        while True:
            res, frame = cap.read()
            if not res:
                break
            liste_frames.append(frame)
        
        cap.release()
    else:
        print("Invalid path")
        return []
    
    return liste_frames

def save_video(output_video_frames, output_video_path):
    if not output_video_frames:
        print("No frames to save.")
        return

    # Ensure the directory exists
    output_dir = os.path.dirname(output_video_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    frame_size = (output_video_frames[0].shape[1], output_video_frames[0].shape[0])
    out = cv2.VideoWriter(output_video_path, fourcc, 24, frame_size)
    
    if not out.isOpened():
        print(f"Error opening video writer for path: {output_video_path}")
        return
    
    for frame in output_video_frames:
        out.write(frame)
    
    out.release()
    print(f"Video saved to {output_video_path}")
