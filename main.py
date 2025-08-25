# -*- coding: utf-8 -*-
from utils import read_video, save_video
from tracker import PlayerTracker  
from tracker import BallTracker
from court_line_detector import CourtLineDetector
from petit_terrain import Petit_Terrain
import os

def main():
    print("Starting video processing")
    court_model_path=r"C:\Users\PC_DHIA\Desktop\tennisballprojectcv\models\keypoints_model.pth"
    # Assurez-vous que le modèle existe à l'emplacement spécifié
    player_trackerx = PlayerTracker(r'C:\Users\PC_DHIA\Desktop\tennisballprojectcv\models\yolov8m.pt')
    ball_tracker=BallTracker(r"C:\Users\PC_DHIA\Desktop\tennisballprojectcv\models\bestmu_36.pt")
    # Lecture de la vidéo d'entrée
    input_video = r'C:\Users\PC_DHIA\Desktop\tennisballprojectcv\input_video\input_video.mp4'
    video_frames = read_video(input_video)
    petit_terrain=Petit_Terrain(30,20,video_frames[0])
    # Spécifier le chemin pour enregistrer les boîtes de détection
    path_fichier = r'C:\Users\PC_DHIA\Desktop\tennisballprojectcv\input_video\databboxes.pkl'
    path_ball_fichier=r'C:\Users\PC_DHIA\Desktop\tennisballprojectcv\input_video\databboxes_ball.pkl'
    list_dict=player_trackerx.track_frames(video_frames, read_from_path=True, path_video=path_fichier)
    ball_dict=ball_tracker.trackball_frames(video_frames,read_from_path=True,path_video=path_ball_fichier)
    court_line_detector = CourtLineDetector(court_model_path)
    court_keypoints = court_line_detector.predict(video_frames[0])
    
    # Assurez-vous que le répertoire de sortie existe
    output_dir = r'C:\Users\PC_DHIA\Desktop\tennisballprojectcv\outputvideos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    id_players=player_trackerx.Find_Players(list_dict, court_keypoints)
    
    print("#########################################")
    list_dict=player_trackerx.get_bboxfromid(id_players,list_dict)
    print(list_dict)
    print("########################################")
    ball_dict=ball_tracker.interpolate_function(ball_dict)
    player_mini_court_detections, ball_mini_court_detections=petit_terrain.courte_distance_frames(list_dict,court_keypoints,ball_dict)
    list_frames=player_trackerx.draw_bbox(list_dict, video_frames)
    list_frames=ball_tracker.draw_bboxes(ball_dict, video_frames)
    list_frames=petit_terrain.draw_lignes_points_in_frames(list_frames)
    list_frames= petit_terrain.draw_points_on_mini_court(list_frames,player_mini_court_detections)
    list_frames= petit_terrain.draw_points_on_mini_court(list_frames,ball_mini_court_detections,color=(0,255,255))
    output_video_frames  = court_line_detector.draw_keypoints_on_video(list_frames, court_keypoints)
    # Spécifiez le chemin de la vidéo de sortie
    output_path = os.path.join(output_dir, 'output_video20.avi')
    
    save_video(output_video_frames , output_path)
    #print("========================================<<>>",ball_dict)
    #print("************",type(ball_dict))
if __name__ == "__main__":
    main()
