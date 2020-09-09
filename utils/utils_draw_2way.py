import numpy as np
import cv2

from utils.utils_color import COLOR_TABEL_LINE
from utils.utils_color import COLOR_TABEL_OB

X0 = 30
Y0 = 30

d_row 	= 35
d_clo 	= 70


COLOR_WHITE     = (255, 255, 255)
COLOR_RED       = (0, 0, 255)
COLOR_GREEN     = (0, 255, 0)
COLOR_BLUE      = (255, 0, 0)
COLOR_PURPLE    = (255, 0, 255)
COLOR_YELLOW    = (0, 255, 255)
COLOR_YELLOW1    = (135, 255, 255)
COLOR_YELLOW2    = (135, 135, 255)

COLOR_TABEL = [COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_PURPLE, COLOR_YELLOW,COLOR_YELLOW1,COLOR_YELLOW2]



def draw_no_object(frame,obiect_index, per_up, per_down,  index) :

    cv2.putText(frame, "frontward",           (X0  + 3*d_clo              ,Y0 ),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_LINE[1], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, "backward",             (X0  + 4*d_clo + d_clo      ,Y0 ),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_LINE[1], 2, lineType=cv2.LINE_AA)

    cv2.putText(frame, obiect_index,            (X0                         ,Y0 + 40 + index*d_row),cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TABEL_OB[index], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(per_up),             (X0 + 3*d_clo               ,Y0 + 40 + index*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[index], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(per_down),           (X0 + 4*d_clo  + d_clo      ,Y0 + 40 + index*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[index], 2, lineType=cv2.LINE_AA)




def draw_no_object_zone(frame,obiect_index, counter_no, index) :

    cv2.putText(frame, "counter",           (X0  + 3*d_clo              ,Y0 ),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_LINE[1], 2, lineType=cv2.LINE_AA)

    cv2.putText(frame, obiect_index,            (X0                         ,Y0 + 40 + index*d_row),cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TABEL_OB[index], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(counter_no),             (X0 + 3*d_clo               ,Y0 + 40 + index*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[index], 2, lineType=cv2.LINE_AA)




if __name__ =='__main__' :

    # Create a black image
    img = np.zeros((200,800,3), np.uint8)
    draw_title(img)
    draw_no_object(img, 1,2,3454,4344,424,243,73,3,92,13,0)
    draw_no_next_id(img,122,43,54,45,345,0)
    draw_no_current(img,122,43,54,45,345,0)
    # img = cv2.resize(img, (600,100))
    cv2.imshow('a',img)
    k = cv2.waitKey(0)
    # Press q to break
    # if k == ord('q'):
        # break