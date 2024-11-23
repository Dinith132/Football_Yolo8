import sys
sys.path.append("../")
from utils import measure_distance, get_center_of_bbox

class PlayerBallAssigner:
    def __init__(self):
        self.max_player_ball_distance=70

    def assign_ball_to_player(self, players, ball_box):
        # print("================================")
        # print(ball_box)
        # print("================================")

        ball_position=get_center_of_bbox(ball_box)

        minimun_distance=99999
        assign_player=-1

        for player_id, player in players.items():
            player_box=player["box"]

            left=measure_distance((player_box[0],player_box[-1]),ball_position)
            right=measure_distance((player_box[2],player_box[-1]),ball_position)
            distance=min(left, right)

            if distance<self.max_player_ball_distance:
                if distance<minimun_distance:
                    minimun_distance=distance
                    assign_player=player_id 

        return assign_player


