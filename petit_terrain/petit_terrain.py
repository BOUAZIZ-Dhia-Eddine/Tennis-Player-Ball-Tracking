import cv2
import sys
sys.path.append("../")
import Les_Constantes as ls
from utils import (find_center, find_distance, calcul_foot, calcul_position, 
                   get_height_of_bbox, convert_pixel_distance_to_meters, 
                    convert_from_metre_to_pixel, 
                   )

class Petit_Terrain: 
    def __init__(self, marge, padding, frame, width=250, height=450):
        self.width_terrain = width
        self.height_terrain = height
        self.marge = marge
        self.padding = padding
        self.frame = frame 
        self.color_stade = (34, 34, 178)  # Couleur rouge brique
        self.creation_rectangle()
        self.set_court_lines()
        self.set_points_miniterrain()
         
    def creation_rectangle(self):
        _, w, h = self.frame.shape
        self.start_x = self.marge
        self.start_y = self.marge
        self.end_x = self.start_x + self.width_terrain
        self.end_y = self.start_y + self.height_terrain

    def set_points_miniterrain(self):
        # Dimensions du terrain en pixels
        terrain_width_in_pixels = convert_from_metre_to_pixel(ls.width_terrain)
        terrain_height_in_pixels = convert_from_metre_to_pixel(ls.demi_length_terrain * 2)

        # Calculer les décalages pour un padding uniforme sur les quatre côtés
        terrain_center_x = self.start_x + (self.width_terrain - terrain_width_in_pixels) // 2
        terrain_center_y = self.start_y + (self.height_terrain - terrain_height_in_pixels) // 2

        # Points du terrain
        self.point0 = (int(terrain_center_x), int(terrain_center_y + self.padding))
        self.point1 = (int(self.point0[0] + terrain_width_in_pixels), int(self.point0[1]))
        self.point2 = (int(self.point0[0]), int(self.point0[1] + terrain_height_in_pixels - self.padding * 2))
        self.point3 = (int(self.point1[0]), int(self.point2[1]))
        self.point4 = (int(self.point0[0] + convert_from_metre_to_pixel(ls.double_ally_differ)), int(self.point0[1]))
        self.point5 = (int(self.point4[0]), int(self.point2[1]))
        self.point6 = (int(self.point1[0] - convert_from_metre_to_pixel(ls.double_ally_differ)), int(self.point0[1]))
        self.point7 = (int(self.point6[0]), int(self.point2[1]))
        self.point8 = (int(self.point4[0]), int(self.point4[1] + convert_from_metre_to_pixel(ls.length_1_zone)))
        self.point9 = (int(self.point6[0]), int(self.point8[1]))
        self.point10 = (int(self.point4[0]), int(self.point5[1] - convert_from_metre_to_pixel(ls.length_1_zone)))
        self.point11 = (int(self.point6[0]), int(self.point10[1]))
        self.point12 = (int((self.point8[0] + self.point9[0]) / 2), int(self.point8[1]))
        self.point13 = (int((self.point10[0] + self.point11[0]) / 2), int(self.point10[1]))
         
    def draw_lignes_points_terrain_in_frame(self, frame):
        # Dessiner les lignes 
        cv2.rectangle(frame, self.point0, self.point3, self.color_stade, -1)
        cv2.line(frame, (self.point0[0], int((self.point0[1] + self.point2[1]) / 2)), 
                 (self.point1[0], int((self.point1[1] + self.point3[1]) / 2)), (0, 255, 255), 2)
        for tup in self.lines:
            point1 = getattr(self, f'point{tup[0]}')
            point2 = getattr(self, f'point{tup[1]}')
            cv2.line(frame, point1, point2, (255, 255, 255), 2)
        # Dessiner les points : 
        for i in range(14):
            point = getattr(self, f'point{i}')
            cv2.circle(frame, point, 5, (255, 0, 0), -1)
        return frame 
     
    def draw_lignes_points_in_frames(self, frames):
        out_frames = []
        for frame in frames: 
            frame = self.draw_background_rectangle(frame)
            frame = self.draw_lignes_points_terrain_in_frame(frame)
            out_frames.append(frame)
        return out_frames
                         
    def set_court_lines(self):
        self.lines = [
            (0, 2),
            (4, 5),
            (6, 7),
            (1, 3),
            (0, 1),
            (8, 9),
            (10, 11),
            (2, 3),
            (12, 13)
        ]
           
    def draw_background_rectangle(self, frame):
        image_copy = frame.copy()
        color_background = (255, 255, 255)
        # Dessiner le rectangle blanc avec transparence
        cv2.rectangle(image_copy, (self.start_x, self.start_y), (self.end_x, self.end_y), color_background, -1)
        alpha = 0.5  # Ajuster la transparence si nécessaire
        frame = cv2.addWeighted(image_copy, alpha, frame, 1 - alpha, 0)
        return frame
    
    def position_mini_terrain(self, player_position, courte_proche, cp, player_high_meters, max_player_height_in_pixels):
        # Calcul des différences en x et y entre la position du joueur et le point court
        diff_x, diff_y = calcul_position(player_position, cp)

        # Conversion des différences de pixels en mètres
        diff_x = convert_pixel_distance_to_meters(diff_x, player_high_meters, max_player_height_in_pixels)
        diff_y = convert_pixel_distance_to_meters(diff_y, player_high_meters, max_player_height_in_pixels)

        # Conversion des distances en mètres vers des pixels pour les coordonnées sur le court
        distance_x_court = convert_from_metre_to_pixel(diff_x)
        distance_y_court = convert_from_metre_to_pixel(diff_y)

        # Correction du point de référence (vérification si courte_proche est correct)
        position = getattr(self, f'point{courte_proche}')

        # Retourne la nouvelle position en ajoutant les distances calculées
        return (position[0] + distance_x_court, position[1] + distance_y_court+20)

    def courte_distance_player_dans_frame(self, pf, court_points, list_court=[0, 2, 13, 12]):
        # Calcul correct des distances entre chaque point du court et le joueur
      liste_p = []
    
      for court in list_court:
            cp = (court_points[court * 2], court_points[court * 2 + 1])
            
            # Calcul de la distance entre le joueur et le point court
            distance = find_distance(pf, cp)
            
            # Ajouter les informations de distance à la liste
            liste_p.append([court, cp, distance])

        # Trier la liste des distances par ordre croissant pour trouver le plus proche
      liste_p = sorted(liste_p, key=lambda x: x[2])[0][0:2]

      return liste_p


    def courte_distance_frames(self, players_tracks, court_points, ball_boxes):
        player_heights = {
            1: ls.PLAYER_1_HEIGHT_METERS,
            4: ls.PLAYER_2_HEIGHT_METERS
        }
        output_player_boxes = []
        output_ball_boxes = []

        # Pour chaque frame dans les pistes de joueurs
        for frame, frame_tracker in enumerate(players_tracks):
            ball_box = ball_boxes[frame][1]
            ball_position = find_center((ball_box[0], ball_box[1]), (ball_box[2], ball_box[3]))
            closest_player_id_to_ball = min(frame_tracker.keys(), key=lambda x: find_distance(ball_position, find_center((frame_tracker[x][0],frame_tracker[x][1]),(frame_tracker[x][2],frame_tracker[x][3]))))

            # Pour chaque joueur dans la frame
            output_player_bboxes_dict = {}
            for player_id, bboxes in frame_tracker.items():
                # Calcul de la position du pied du joueur
                pf = calcul_foot(bboxes)
                
                # Trouver la courte la plus proche pour ce joueur
                courte_proche, cp_position = self.courte_distance_player_dans_frame(pf, court_points)

                # Calcul de la hauteur maximale des bounding boxes du joueur dans les frames spécifiées
                frame_index_min = max(0, frame - 20)
                frame_index_max = min(len(players_tracks), frame + 50)
                bboxes_heights_in_pixels = [get_height_of_bbox(players_tracks[i][player_id]) for i in range(frame_index_min, frame_index_max) if player_id in players_tracks[i]]
                max_player_height_in_pixels = max(bboxes_heights_in_pixels) if bboxes_heights_in_pixels else 0

                # Calcul de la position du joueur sur le mini terrain
                player_court_position = self.position_mini_terrain(pf, courte_proche, cp_position,
                                                                   player_heights[player_id], max_player_height_in_pixels)
                # Ajouter la position calculée au dictionnaire des positions
                output_player_bboxes_dict[player_id] = player_court_position

                if closest_player_id_to_ball == player_id:
                    # Calcul pour la balle
                    courte_proche_ball, cp_position_ball = self.courte_distance_player_dans_frame(ball_position, court_points)
                    mini_court_player_position = self.position_mini_terrain(ball_position,
                                                                            courte_proche_ball, 
                                                                            cp_position_ball, 
                                                                            player_heights[player_id],
                                                                            max_player_height_in_pixels)
                    output_ball_boxes.append({1: mini_court_player_position})

            output_player_boxes.append(output_player_bboxes_dict)

        return output_player_boxes, output_ball_boxes
    def draw_points_on_mini_court(self,frames,postions, color=(0,255,0)):
      for frame_num, frame in enumerate(frames):
          for _, position in postions[frame_num].items():
              x,y = position
              x= int(x)
              y= int(y)
              cv2.circle(frame, (x,y), 5, color, -1)
      return frames
