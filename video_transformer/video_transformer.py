import numpy as np
import cv2

class VidoeTransformer():
    def __init__(self):
       court_width=68
       court_length=23.32

       self.pixel_vertices=np.array([
           [110,1035],
           [265,275],
           [910,260],
           [1640,915]
       ], dtype=np.float32) 
       
       self.target_vertices=np.array([
           [0,court_width],
           [0 ,0],
           [court_length,0],
           [court_length,court_width]
       ], dtype=np.float32)

    #    self.pixel_vertices=self.pixel_vertices.astype(np.float32)
    #    self.target_vertices_vertices=self.target_vertices.astype(np.float32)

       self.perspective_trnsformer=cv2.getPerspectiveTransform(self.pixel_vertices, self.target_vertices)


    def transform_point(self, point):
        point_int = tuple(map(int, point))
        if cv2.pointPolygonTest(self.pixel_vertices, point_int, False) < 0:
            return None
        
        point_reshaped = np.array([[point]], dtype=np.float32)
        transformed_point = cv2.perspectiveTransform(point_reshaped, self.perspective_trnsformer)
        return transformed_point[0, 0]
    
    def add_transformed_position_to_tracks(self,tracks):
        for object, object_track in tracks.items():
            for frame_num, track in enumerate(object_track):
                for track_id, track_info in  track.items():
                    position= track_info['adjusted_posistion']
                    position=np.array(position)
                    # print("================================================================")
                    # print(object)
                    # print(position)

                    position_transformed= self.transform_point(position)
                    # print(position_transformed)
                    # print("================================================================")

                    if position_transformed is not None:
                        position_transformed=position_transformed.squeeze().tolist()
                    tracks[object][frame_num][track_id]['position_transformed']=position_transformed
                    # print(position_transformed)
        return tracks
