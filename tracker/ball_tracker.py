# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 13:53:10 2024

@author: PC_DHIA
"""

# -*- coding: utf-8 -*-

import pickle
import cv2
import numpy as np
from ultralytics import YOLO
from filterpy.kalman import KalmanFilter
import pandas as pd 
class BallTracker():
    def __init__(self, path_model, conf=0.15, save=True):
        self.model = YOLO(path_model)
        self.conf = conf
        self.save = save   
        

    def interpolate_function(self, list_dict):
        if list_dict:
        # Définition du filtre de Kalman
           kf = KalmanFilter(dim_x=8, dim_z=4)
           dt = 1.0  # intervalle de temps entre les images
           # Matrice de transition de l'état (F)
           kf.F = np.array([
            [1, 0, 0, 0, dt,  0,  0,  0],
            [0, 1, 0, 0,  0, dt,  0,  0],
            [0, 0, 1, 0,  0,  0, dt,  0],
            [0, 0, 0, 1,  0,  0,  0, dt],
            [0, 0, 0, 0,  1,  0,  0,  0],
            [0, 0, 0, 0,  0,  1,  0,  0],
            [0, 0, 0, 0,  0,  0,  1,  0],
            [0, 0, 0, 0,  0,  0,  0,  1]
        ])
           # Matrice de mesure (H)
           kf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0]
        ])
           # Covariance du bruit de processus (Q) et de mesure (R)
           kf.P *= 1000.  # incertitude initiale
           kf.R *= 5.     # incertitude de mesure
           kf.Q *= 0.01   # bruit de processus

           for i, d in enumerate(list_dict):
              if d:  # Si le dictionnaire n'est pas vide
                  if i == 0:
                    # Si le premier dictionnaire est non vide, initialisation
                      x1, y1, x2, y2 = d[1]
                      kf.x[:4] = np.array([x1, y1, x2, y2]).reshape(-1, 1)
                  else:
                    # Mise à jour du filtre de Kalman avec les nouvelles mesures
                      kf.update(d[1])
              else:
                  if i == 0:
                      x1, y1, x2, y2 = list_dict[1][1]
                      x11, y11, x22, y22 = x1 +30,y1-20,x2-5,y2 -20
                      kf.x[:4] =np.array([x11, y11, x22, y22]).reshape(-1, 1) 
                      list_dict[0][1]=np.array([x11,y11,x22,y22]).reshape(-1).tolist()
                  else:
                      kf.predict()
                      list_dict[i][1] = kf.x[:4].reshape(-1).tolist()
        return list_dict 

    # pour un seul frame
    def trackball_frame(self, frame):
        # Traiter le cadre avec le modèle de suivi
        results = self.model.predict(frame, conf=self.conf, save=self.save)[0]
        ball_detect={}
        for box in results.boxes:
            result = box.xyxy.tolist()[0]
            ball_detect[1]= result
        return ball_detect

    # pour toutes les frames
    def trackball_frames(self, listes_frames, read_from_path=False, path_video=None):
        listes_bbox_perframe = []

        if path_video is not None:
            # Lire à partir du fichier
            if read_from_path:
                with open(path_video, 'rb') as f:
                    listes_bbox_perframe = pickle.load(f)
                return listes_bbox_perframe

            if listes_frames:
                for frame in listes_frames:
                    listes_bbox_perframe.append(self.trackball_frame(frame))

                with open(path_video, 'wb') as f:
                    pickle.dump(listes_bbox_perframe, f)
                return listes_bbox_perframe
            else:
                print("La liste des frames est vide !")
        else:
            print('Le chemin du fichier vidéo est None.')

    def draw_bboxes(self, player_detections,video_frames):
        output_video_frames = []
        for frame, ball_dict in zip(video_frames, player_detections):
            # Draw Bounding Boxes
            for track_id, bbox in ball_dict.items():
                x1, y1, x2, y2 = bbox
                cv2.putText(frame, f"Ball ID: {track_id}",(int(bbox[0]),int(bbox[1] -10 )),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
            output_video_frames.append(frame)
        
        return output_video_frames
    
    def get_ball_shot_frames(self,ball_positions):
        ball_positions = [x.get(1,[]) for x in ball_positions]
        # convert the list into pandas dataframe
        df_ball_positions = pd.DataFrame(ball_positions,columns=['x1','y1','x2','y2'])

        df_ball_positions['ball_hit'] = 0

        df_ball_positions['mid_y'] = (df_ball_positions['y1'] + df_ball_positions['y2'])/2
        df_ball_positions['mid_y_rolling_mean'] = df_ball_positions['mid_y'].rolling(window=5, min_periods=1, center=False).mean()
        df_ball_positions['delta_y'] = df_ball_positions['mid_y_rolling_mean'].diff()
        minimum_change_frames_for_hit = 25
        for i in range(1,len(df_ball_positions)- int(minimum_change_frames_for_hit*1.2) ):
            negative_position_change = df_ball_positions['delta_y'].iloc[i] >0 and df_ball_positions['delta_y'].iloc[i+1] <0
            positive_position_change = df_ball_positions['delta_y'].iloc[i] <0 and df_ball_positions['delta_y'].iloc[i+1] >0

            if negative_position_change or positive_position_change:
                change_count = 0 
                for change_frame in range(i+1, i+int(minimum_change_frames_for_hit*1.2)+1):
                    negative_position_change_following_frame = df_ball_positions['delta_y'].iloc[i] >0 and df_ball_positions['delta_y'].iloc[change_frame] <0
                    positive_position_change_following_frame = df_ball_positions['delta_y'].iloc[i] <0 and df_ball_positions['delta_y'].iloc[change_frame] >0

                    if negative_position_change and negative_position_change_following_frame:
                        change_count+=1
                    elif positive_position_change and positive_position_change_following_frame:
                        change_count+=1
            
                if change_count>minimum_change_frames_for_hit-1:
                    df_ball_positions['ball_hit'].iloc[i] = 1

        frame_nums_with_ball_hits = df_ball_positions[df_ball_positions['ball_hit']==1].index.tolist()

        return frame_nums_with_ball_hits
                 
                     
            