from ultralytics import YOLO
import supervision as sv
import pickle
import os
import sys
sys.path.append('../')
from utils import get_center_of_bbox,get_width_of_bbox,get_foot_position
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Tracker:
    def __init__(self, model_path):
        self.model=YOLO(model_path)
        self.tracker=sv.ByteTrack()
        # print("dof,dl,dl;,d;l,d;ll;")

    def add_position_to_tracks(self, tracks):
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    bbox=track_info['box']
                    if object=="ball":
                        posistion=get_center_of_bbox(bbox)
                    else:
                        posistion=get_foot_position(bbox)

                    # print(object)
                    tracks[object][frame_num][track_id]['posistion']=posistion
        
        return tracks
        # print(tracks['ball'])
        

    def interpolate_ball_positions(self, ball_positions):
        ball_positions=[x.get(1,{}).get('box',[]) for x in ball_positions]
        df_ball_positions=pd.DataFrame(ball_positions, columns=['x1','y1','x2','y2'])

        df_ball_positions=df_ball_positions.interpolate()
        df_ball_positions=df_ball_positions.bfill()

        ball_positions=[{1:{"box":x}} for x in df_ball_positions.to_numpy().tolist()]
        return ball_positions
    
    def  detect_frame(self, frames):
        batch_size=30
        detections=[]

        for i in range(0,len(frames),batch_size):
            detections_batch=self.model.predict(frames[i:i+batch_size], conf=0.1)
            detections+=detections_batch
        
        return detections
    
    def get_object_traks(self, frames, read_from_stub=False, stub_path=None): 

        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                tracks=pickle.load(f)
            return tracks

        detections=self.detect_frame(frames)

        tracks={
            "players":[],
            "referees":[],
            "ball":[]
        }

        for frame_num,detection in enumerate(detections):
            cls_names=detection.names
            cls_name_inv={v:k for k,v in cls_names.items()}

            print(cls_names)

            detection_supervision=sv.Detections.from_ultralytics(detection)

            for index,value in enumerate(detection_supervision.class_id):
                if cls_names[value]=="goalkeeper":
                    detection_supervision.class_id[index]=cls_name_inv["player"]

            detection_with_tracks=self.tracker.update_with_detections(detection_supervision)

            tracks["players"].append({})
            tracks["referees"].append({})
            tracks["ball"].append({})

            print(detection_with_tracks)

            for t in detection_with_tracks:
                box=t[0].tolist()
                cls_id=t[3]
                track_id=t[4]

                if cls_id==cls_name_inv['player']:
                    tracks["players"][frame_num][track_id]={"box":box}

                if cls_id==cls_name_inv['referee']:
                    tracks["referees"][frame_num][track_id]={"box":box}

            for t in detection_supervision:
                box=t[0].tolist()
                cls_id=t[3]

                if cls_names[cls_id]=="ball":
                    tracks["ball"][frame_num][1]={"box":box}


        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(tracks,f)

        return tracks
    
    def draw_elipse(self, frame, box, color, track_id=None):
        y2=int(box[3])
        x_center,_=get_center_of_bbox(box)
        width=get_width_of_bbox(box)

        # print(frame)
        cv2.ellipse(
            frame,
            center=(x_center,y2),
            axes=(int(width),int(0.35*width)),
            angle=0.0,
            startAngle=-45,
            endAngle=235,
            color=color,
            thickness=2,
            lineType=cv2.LINE_4
            )
    
        rectangle_width=40
        rectangle_height=20
        x1_rect=x_center-rectangle_width/2
        x2_rect=x_center+rectangle_width/2
        y1_rect=(y2-rectangle_height/2)+15
        y2_rect=(y2+rectangle_height/2)+15

        if track_id is not None:
            
            

            cv2.rectangle(
                frame,
                (int(x1_rect),int(y1_rect)),
                (int(x2_rect),int(y2_rect)),
                color,
                cv2.FILLED
            )

            x1_text=x1_rect+12
            if track_id>10:
                x1_text=x1_rect+6
            
            cv2.putText(
                frame,
                f"{track_id}",
                (int(x1_text),int(y2_rect-5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,0,0),
                2
            )

        
        return frame

    def draw_trangle(self, frame, box, color):
        x_center,_=get_center_of_bbox(box)
        y1=int(box[1])-5

        trangle_width=12
        trangle_height=12

        trangle_points=np.array([
            [x_center,y1],
            [x_center-trangle_width/2,y1-trangle_height],
            [x_center+trangle_width/2,y1-trangle_height]

        ])

        trangle_points = trangle_points.astype(np.int32)
        trangle_points=trangle_points.reshape((-1,1,2))

        cv2.drawContours(frame, [trangle_points], 0, color, cv2.FILLED)
        cv2.drawContours(frame, [trangle_points], 0, (0,0,0), 2)

        return frame

    def draw_annotation(self,video_frames, tracks, team_ball_control):
        output_video_frame=[]

        for frame_num, frame in enumerate(video_frames):
            frame =frame.copy()

            player_dict=tracks["players"][frame_num]
            ball_dict=tracks["ball"][frame_num]
            referee_dict=tracks["referees"][frame_num]


            for track_id, player in player_dict.items():
                color=player.get("team_color",(0,0,225))
                frame=self.draw_elipse(frame, player["box"], player["team_color"], track_id)

                if player.get("has_ball", False):
                    frame=self.draw_trangle(frame, player["box"], (0,0,255))

            for track_id, referee in referee_dict.items():
                frame=self.draw_elipse(frame, referee["box"], (51,51,225))

            for _,ball in ball_dict.items():
                frame=self.draw_trangle(frame, ball["box"],(0,255,0))
            
            frame=self.draw_team_ball_control(frame, frame_num, team_ball_control)

            output_video_frame.append(frame)

        return output_video_frame
    
    def draw_team_ball_control(self, frame, frame_num, team_ball_control):
        overlay=frame.copy()
        cv2.rectangle(overlay, (1350,850),(1900, 970),(255,255,255),-1)
        alpha= 0.4
        cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0, frame)

        team_ball_control_till_frame=team_ball_control[:frame_num+1]
        team_1_num_frames= team_ball_control_till_frame[team_ball_control_till_frame==1].shape[0] 
        team_2_num_frames= team_ball_control_till_frame[team_ball_control_till_frame==2].shape[0]

        team_1= team_1_num_frames/(team_1_num_frames+team_2_num_frames)
        team_2= team_2_num_frames/(team_1_num_frames+team_2_num_frames)

        cv2.putText(frame, f"Team 1 Ball Control: {team_1*100:2f}%",(1400,900), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
        cv2.putText(frame, f"Team 2 Ball Control: {team_2*100:2f}%",(1400,950), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)

        return overlay