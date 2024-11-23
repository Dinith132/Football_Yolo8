import cv2
from sklearn.cluster import KMeans
import numpy as np

class TeamAssigner:
    def __init__(self):
        self.team_colors={}
        self.player_team_dict={}

    def get_cluster_models(self, image):
        image_2d=image.reshape(-1,3)
        kmeans=KMeans(n_clusters=2,init="k-means++", n_init=10, random_state=42, algorithm='elkan')
        kmeans.fit(image_2d)

        return kmeans

    def get_player_color(self, frame, box):
        # print("======================================================")

        
        # print(box)
        # print("======================================================")

        
        croped=frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
        # croped=cv2.cvtColor(croped)

        half=croped[0:int(croped.shape[1]/2), :]
        half=cv2.cvtColor(half, cv2.COLOR_BGR2RGB)
        kmeans= self.get_cluster_models(half)

        labels=kmeans.labels_

        # print("======================================================")
        # print(half.shape)
        

        labels=labels.reshape(half.shape[0],half.shape[1])
        coners=[labels[0][0],labels[-1][0],labels[0][-1],labels[-1][-1]]
        
        back_cluster=max(set(coners), key=coners.count)
        player_cluster=1-back_cluster

        return kmeans.cluster_centers_[player_cluster]

    def assign_team_color(self, frame, player_detections):
        player_colors=[]
        for _,player_detection in player_detections.items():
            box=player_detection["box"]
            player_color=self.get_player_color(frame, box)
            player_colors.append(player_color)
 
        
        kmeans=KMeans(n_clusters=2, init="k-means++", n_init=1)
        kmeans.fit(player_colors)

        self.kmeans=kmeans

        self.team_colors[1]=kmeans.cluster_centers_[0]
        self.team_colors[2]=kmeans.cluster_centers_[1]

        # self.team_colors[1]=(0,0,255)
        # self.team_colors[2]=(255,0,0)

    def get_player_team(self,frame, player_bbox,player_id):
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]
        
        player_color= self.get_player_color(frame, player_bbox["box"])

        team_id=self.kmeans.predict(player_color.reshape(1,-1))[0]
        team_id+=1

        self.player_team_dict[player_id]=team_id

        return team_id