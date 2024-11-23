from utils import read_video,save_video
from trackers import Tracker
import cv2
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
import numpy as np
from camera_movement_estimator import CameramovementEstimeter
from video_transformer import VidoeTransformer
from speed_and_distance_astimater import SpeedAndDistanceEstimate

def main():
  model_path="models/best.pt"
  intput_path="input_videos/input.mp4"

  frames=read_video(intput_path)

  tracker=Tracker(model_path)
  tracks=tracker.get_object_traks(frames,read_from_stub=True,stub_path="stubs/track_stubs.pkl")
  tracks=tracker.add_position_to_tracks(tracks)

  cam_movement_estimator=CameramovementEstimeter(frames[0])
  cam_movement_per_frame= cam_movement_estimator.get_camera_movement(frames,read_from_stub=True,stub_path="stubs/camera_movement_stub.pkl")

  tracks=cam_movement_estimator.add_adjustment_posistion(tracks,cam_movement_per_frame)

  view_transformer=VidoeTransformer()
  tracks=view_transformer.add_transformed_position_to_tracks(tracks)

  # print(tracks)
  
  tracks["ball"]=tracker.interpolate_ball_positions(tracks["ball"])

  speed_and_distance=SpeedAndDistanceEstimate()
  tracks=speed_and_distance.add_speed_and_distance_to_tracks(tracks)

  teamassigner=TeamAssigner()
  teamassigner.assign_team_color(frames[0],tracks["players"][0])

  for frame_num,player_track in enumerate(tracks["players"]):
    for player_id, track in player_track.items():
      team= teamassigner.get_player_team(frames[frame_num],track,player_id)

      tracks['players'][frame_num][player_id]["team"]=team
      tracks['players'][frame_num][player_id]["team_color"]=teamassigner.team_colors[team]

  player_assiner=PlayerBallAssigner()
  team_ball_control=[]

  for frame_num, player_track in enumerate(tracks["players"]):
    ball_possition=tracks["ball"][frame_num][1]["box"]
    assingned_player=player_assiner.assign_ball_to_player(player_track,ball_possition)

    if assingned_player !=-1:
      tracks['players'][frame_num][assingned_player]['has_ball']=True
      team_ball_control.append(tracks["players"][frame_num][assingned_player]['team'])
    else:
      team_ball_control.append(team_ball_control[-1])

  team_ball_control=np.array(team_ball_control)

  # player_assiner.assign_ball_to_player(tracks["players"],tracks["ball"])
  # # print(tracks)

  output_frames=tracker.draw_annotation(frames,tracks,team_ball_control)

  # output_frames=cam_movement_estimator.draw_camera_movement(output_frames,cam_movement_per_frame)
  # output_frames=speed_and_distance.draw_speed_and_distance(output_frames,tracks)

  output_path="output_video/out.avi"
  save_video(output_frames,output_path) 

  # print(tracks)






if __name__=='__main__':
  main()