# -*- coding: utf-8 -*-

import pickle
import cv2
from ultralytics import YOLO
import sys
sys.path.append('../')
from utils import find_center, find_distance
class PlayerTracker():
    def __init__(self, path_model, persist=True, conf=0.2, save=True):
        self.model = YOLO(path_model)
        self.persist = persist
        self.conf = conf
        self.save = save

    # pour un seul frame
    def track_frame(self, frame):
        # Traiter le cadre avec le modèle de suivi
        results = self.model.track(frame, conf=self.conf, persist=self.persist, save=self.save)[0]

        # Obtenir les noms de classes comme un dictionnaire (id_classe: nom)
        class_names = results.names

        # Initialiser une liste pour stocker les boîtes des personnes
        tracks_players = dict()

        # Parcourir les boîtes détectées
        for box in results.boxes:
            # Obtenir les identifiants et les coordonnées
            track_id = int(box.id.tolist()[0])
            xyxy = box.xyxy.tolist()[0]
            cls_id = int(box.cls.tolist()[0])
            name_class_box = class_names[cls_id]

            # Vérifier si la détection est une personne et si le score de confiance est suffisant
            if name_class_box == "person" and box.conf.tolist()[0] >= self.conf:
                # Ajouter les coordonnées de la boîte à la liste
                tracks_players[track_id] = xyxy

        return tracks_players

    # pour toutes les frames
    def track_frames(self, listes_frames, read_from_path=False, path_video=None):
        listes_bbox_perframe = []

        if path_video is not None:
            # Lire à partir du fichier
            if read_from_path:
                with open(path_video, 'rb') as f:
                    listes_bbox_perframe = pickle.load(f)
                return listes_bbox_perframe

            if listes_frames:
                for frame in listes_frames:
                    listes_bbox_perframe.append(self.track_frame(frame))

                with open(path_video, 'wb') as f:
                    pickle.dump(listes_bbox_perframe, f)
                return listes_bbox_perframe
            else:
                print("La liste des frames est vide !")
        else:
            print('Le chemin du fichier vidéo est None.')

    def draw_bbox(self, list_dict, video_frames):
        if list_dict and video_frames:
            list_frames = []
            for dict_frame, frame in zip(list_dict, video_frames):
                for key, value in dict_frame.items():
                    cv2.rectangle(frame, (int(value[0]), int(value[1])), (int(value[2]), int(value[3])), (0, 0, 255), 2)
                    cv2.putText(frame, f"id:{key}", (int(value[0]), int(value[1]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                list_frames.append(frame)

            return list_frames

    def Find_Players(self, players_track, list_despoints, distance_threshold=250):
        set_player_id = set()
        players_track_center = []

        # Calculer le centre pour chaque personne présente dans chaque frame
        for dic in players_track:
            list_frame = [{key: find_center((value[0], value[1]), (value[2], value[3])) for key, value in dic.items()}]
            players_track_center.append(list_frame)

        # Calculer les distances pour chaque personne dans chaque frame
        listes_dist_t_frame = []
        for frame in players_track_center:
            listes_per_dist_fr = []

            for person_id, center in frame[0].items():
                distances_per = []

                for i in range(0, len(list_despoints), 2):
                    keypoint = (list_despoints[i], list_despoints[i + 1])
                    distances_per.append(find_distance(keypoint, center))

                # Stocker les distances par personne
                listes_per_dist_fr.append((person_id, sorted(distances_per)))

            listes_dist_t_frame.append(listes_per_dist_fr)

        # Déterminer quels joueurs sont les plus proches des points clés
        for frame in listes_dist_t_frame:
            frame.sort(key=lambda x: x[1][0])  # Trier les distances par ordre croissant

            # Ne considérer que les deux joueurs les plus proches ou ceux dans un seuil de distance
            for person_id, distances in frame[:2]:  # Prendre les deux personnes les plus proches
                if distances[0] < distance_threshold:
                    set_player_id.add(person_id)

        return set_player_id
    
    def get_bboxfromid(self,set_player_id,player_track): 
        player_track2=[]
        for frame in player_track: 
            dict_2=dict()
            for key,value in frame.items():
                if key in set_player_id:
                    dict_2[key]=value 
            player_track2.append(dict_2)
        return player_track2 

              
        
    
                    
                    
