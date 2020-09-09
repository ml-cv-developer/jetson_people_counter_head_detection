from shapely.geometry import Point, Polygon
import cv2
import numpy as np
from skimage.draw import line, polygon, circle, ellipse
# func_note = '579,258,7,600,174,719,1266,719,1270,403,1056,253'

from utils.utils_color import COLOR_TABEL_LINE
from utils.utils_color import COLOR_TABEL_OB



def decode_note_counter_line(func_note) :

    points  = func_note.split(",")
    if len(points) != 8 :
        print(points)
        raise "Error Format len point of counter line" 

    line    = points[0:4]
    point   = points[4:8]
    
    line = [int(float(x)) for x in line]
    point = [int(float(x)) for x in point]

    return line, point

    
def decode_note_counter(func_note) :

    points  = func_note.split(",")
    if len(points) != 4 :
        print(points)
        raise "Error Format len point of counter line" 

    line    = points[0:4]
    
    line = [int(float(x)) for x in line]

    return line

    

def decode_note_polygon(func_note):
    
    point = func_note.split(",")
    point = [int(float(x)) for x in point]
    if len(point) % 2 != 0 :
        print(point)
        raise "Error Format len point of polygon" 

    point = [tuple([point[i], point[i+1]]) for i in range(0, len(point), 2)]

    return point
    

# def decode_take_integer(func_note):
    
#     point = func_note.split(",")
#     point = [int(x) for x in point]
#     if len(point) % 2 != 0 :
#         print(point)
#         raise "Error Format len point of polygon" 

#     point = [tuple([point[i], point[i+1]]) for i in range(0, len(point), 2)]

#     return point



class utils_popygon() :
    def __init__(self, coords) :
        self.polygon    = Polygon(coords)
    
    def isinside(self, bbox) :
        x, y, w, h = bbox
        points = []
        points.append(Point(x, y))
        points.append(Point(x + w, y))
        points.append(Point(x, y + h))
        points.append(Point(x + w, y + h))
        points.append(Point(x + w//2, y + h//2))
        points.append(Point(x + w//2, y + h//4))
        points.append(Point(x + w//4, y + h//2))
        points.append(Point(x + w//4, y + h//4))

        sum_point = 0 
        for point in points :
            if self.polygon.contains(point) :
                sum_point += 1
        
        if sum_point >=2 :
            return True
        else :
            return False
    
    def filter_ob(self,classesid, probs, bboxes) :
        class_new   = []
        bbox_new    = []
        probs_new    = []

        for i, bbox in enumerate(bboxes) :
            if self.isinside(bbox) :
                class_new.append(classesid[i])
                bbox_new.append(bboxes[i])
                probs_new.append(probs[i])
        
        return class_new, probs_new, bbox_new


def draw_polygon(frame, coords,index=10) :
    for i in range(-1, len(coords) - 1) :
        cv2.line(frame, coords[i],coords[i+1], COLOR_TABEL_LINE[index], 2)
        # cv2.line(frame, tuple(coords[i]),tuple(coords[i+1]),(120, 300, 100), 2)
    return frame



def draw_polygon_fill(frame, coords,index=10) :
    h, w, c = frame.shape
    rr, cc = polygon(coords[:,0], coords[:,1], (w, h, c))
    frame[cc, rr] = COLOR_TABEL_LINE[index]
    # frame[cc, rr] = (100, 100, 100)
    return frame
