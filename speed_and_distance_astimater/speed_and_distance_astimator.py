import cv2
import sys
sys.path.append("../")
from utils import measure_distance,get_foot_position


class SpeedAndDistanceEstimate():
    def __init__(self):
        self.frame_window=5
        self.frame_rate=24

    def add_speed_and_distance_to_tracks(self, tracks):
        total_distance={}
        for object, object_tracks in tracks.items():
            if object=='ball' or object=="referees":
                continue
            number_of_frames=len(object_tracks)

            for frame_num in range(0,number_of_frames, self.frame_window):
                last_frame=min(frame_num+self.frame_window, number_of_frames)

                if frame_num >= number_of_frames or last_frame >= number_of_frames:
                    continue


                for track_id in object_tracks[frame_num].keys():
                    if track_id not in object_tracks[last_frame]:
                        continue

                    # print(tracks)
                    start_position=object_tracks[frame_num][track_id]["position_transformed"]
                    end_position=object_tracks[last_frame][track_id]["position_transformed"]

                    

                    if start_position is None or end_position is None:
                        continue

                    distance_covered=measure_distance(start_position, end_position)
                    time_elapsed=(last_frame-frame_num)/self.frame_rate  
                    speed_meteres_per_second=distance_covered /time_elapsed
                    speed_km_per_second=speed_meteres_per_second*3.6

                    if object not in total_distance:
                        total_distance[object]={}

                    if track_id not in total_distance[object]:
                        total_distance[object][track_id]=0

                    total_distance[object][track_id]+=distance_covered

                    for frame_num_batch in range(frame_num, last_frame):
                        if track_id not in tracks[object][frame_num_batch]:
                            continue
                        tracks[object][frame_num][track_id]['speed']=speed_km_per_second
                        tracks[object][frame_num][track_id]['distance']=total_distance[object][track_id]
                        # print(speed_km_per_second)
        return tracks

    # def draw_speed_and_distance(self, frames, tracks):
        output_video_frame=[]

        for frame_num, frame in enumerate(frames):
            for object, object_track in tracks.items():
                if object=='ball' or object=="referees":
                    continue
                for track_id, track_info in object_track[frame_num].items():
                    if 'speed' in track_info:
                        # print("============================================================")
                        speed=track_info['speed']
                        distance=track_info['distance']
                        # print(speed, distance)

                        if speed is None or distance is None:
                            continue

                        bbox=track_info['box']
                        position=get_foot_position(bbox)
                        position=list(position)
                        position[1]+=5

                        position =tuple(map(int,position))
                        cv2.putText(frame, f"Speed: {speed:.2f} km/s", position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                        cv2.putText(frame, f"distance: {distance:.2f} m", (position[0],position[1]+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            output_video_frame.append(frame)
        return output_video_frame

    def draw_speed_and_distance(self, frames, tracks):
        output_video_frame = []

        for frame_num, frame in enumerate(frames):
            for object, object_track in tracks.items():
                if object == 'ball' or object == "referees":
                    continue
                for track_id, track_info in object_track[frame_num].items():
                    if 'speed' in track_info:
                        speed = track_info['speed']
                        distance = track_info['distance']

                        if speed is None or distance is None:
                            continue

                        bbox = track_info['box']
                        foot_position = get_foot_position(bbox)
                        
                        # Calculate position below the player
                        text_position = (int(foot_position[0]), int(bbox[3] + 20))  # 20 pixels below the bottom of the bounding box
                        
                        # Draw speed and distance information
                        cv2.putText(frame, f"Speed: {speed:.2f} km/h", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        cv2.putText(frame, f"Dist: {distance:.2f} m", (text_position[0], text_position[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            output_video_frame.append(frame)
        return output_video_frame