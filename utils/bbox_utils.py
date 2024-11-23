def get_center_of_bbox(box):
    x1,y1,x2,y2=box
    return int((x1+x2)/2), int((y1+y2)/2)

def get_width_of_bbox(box):
    return box[2]-box[0]

def measure_distance(p1,p2):
    return ((p1[0]-p2[0])**2+ (p1[1]-p2[1])**2)**0.5

def get_foot_position(bbox):
    x1,y1,x2,y2 =bbox
    return int(x2+x1), int(y2)

