import pickle
import cv2
import numpy as np
import sys
sys.path.append("../")
from utils import measure_distance
import os

class CameramovementEstimeter():
    def __init__(self, frame):

        self.min_distance =5

        self.lk_params=dict(
            winSize=(15,15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        )   

        first_framw_grayScale=cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        mask_features=np.zeros_like(first_framw_grayScale)
        mask_features[:,0:20]=1
        mask_features[:,900:1050]=1

        self.features=dict(
            maxCorners=100,
            qualityLevel=0.3,
            minDistance=3,
            blockSize=7,
            mask=mask_features
        )


    def add_adjustment_posistion(self,tracks,camera_movement):
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    position=track_info['posistion']
                    adjusted_posistion=(position[0]-camera_movement[frame_num][0],position[1]-camera_movement[frame_num][1])
                    tracks[object][frame_num][track_id]["adjusted_posistion"]=adjusted_posistion
        return tracks
    

    def get_camera_movement(self, frames, read_from_stub=False, stub_path=None):

        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                return pickle.load(f)

        camera_movement=[[0,0]]*len(frames)

        old_gray=cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        old_features=cv2.goodFeaturesToTrack(old_gray, **self.features)

        for frame_num in range(1, len(frames)):
            frames_gray=cv2.cvtColor(frames[frame_num], cv2.COLOR_RGB2GRAY)
            new_features, status, error=cv2.calcOpticalFlowPyrLK(old_gray, frames_gray, old_features, None, **self.lk_params)

            max_distance =0
            camera_movements_x, camera_movements_y=0,0

            for i, (new, old) in enumerate(zip(new_features, old_features)):
                a, b = new.ravel()
                c, d = old.ravel()
                x_distance, y_distance=a-c, b-d
                distance=measure_distance((a,b), (c,d))

                if max_distance<distance:
                    max_distance=distance
                    camera_movements_x, camera_movements_y=x_distance, y_distance
        
            if max_distance>self.min_distance:
                camera_movement[frame_num]=[camera_movements_x, camera_movements_y]
                old_features=cv2.goodFeaturesToTrack(frames_gray, **self.features)
            
            old_gray=frames_gray.copy()

        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(camera_movement, f)

        return camera_movement
    def draw_camera_movement(self, frames, camera_movement_per_frame):
        output_frames = []

        for frame_num, frame in enumerate(frames):
            frame=frame.copy()

            overlay=frame.copy()
            cv2.rectangle(overlay, (0,0),(500, 100),(255,255,255),-1)
            alpha= 0.6
            cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0, frame)

            x_movement, y_movement= camera_movement_per_frame[frame_num]
            frame=cv2.putText(frame, f"Camera Movement x:{x_movement:.2f}" ,(10,30), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,0),3)
            frame=cv2.putText(frame, f"Camera Movement y:{y_movement:.2f}" ,(10,60), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,0),3)

            output_frames.append(frame)

        return output_frames

