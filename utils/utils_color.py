import cv2
import os
import cv2
import time
import numpy as np


COLOR_BLACK       = (0, 0, 0)
COLOR_WHITE       = (255, 255, 255)

COLOR_RED         = (0, 0, 255)
COLOR_RED1        = (0, 125, 255)
COLOR_GREEN       = (0, 255, 0)
COLOR_BLUE        = (255, 0, 0)

COLOR_PURPLE    = (255, 0, 255)
COLOR_PURPLE1   = (255, 255, 0)
COLOR_YELLOW    = (0, 255, 255)

COLOR_YELLOW1    = (255, 255, 0)

COLOR_TABEL = [COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_PURPLE, COLOR_YELLOW]
COLOR_TABEL_OB      = np.random.uniform(100, 255, size=(100, 3))
# COLOR_TABEL_LINE    = np.random.uniform(100, 250, size=(100, 3))
COLOR_TABEL_LINE    = np.random.randint(100, high = 255, size = (100,3)).tolist()
# COLOR_TABEL_OB      = np.random.randint(100, high = 255, size = (100,3)).tolist()
# COLOR_TABEL_OB      = [COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_PURPLE, COLOR_YELLOW, COLOR_PURPLE1, COLOR_YELLOW1]

COLOR_1         = (255, 100, 100)
COLOR_2         = (100, 255, 100)
COLOR_3         = (100, 100, 255)

COLOR_4         = (255, 255, 100)
COLOR_5         = (255, 100, 255)
COLOR_6         = (100, 255, 255)


def draw_object_tracking2(frame, ObjectTracker,label_t, color_id1) :
    # 
    for object_track in ObjectTracker.currentObjects :
        color_id = int(str(object_track.objectID)[-2:])

        # x, y, w, h = object_track.bbox
        x1, y1, x2, y2 = object_track.bbox

        ycenter = object_track.trace[-1][1]
        xcenter = object_track.trace[-1][0]
        
        # cv2.circle(frame, (xcenter, ycenter), 7, COLOR_YELLOW, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2),COLOR_TABEL_OB[color_id1], 2)

        label = "{}".format(label_t)

        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, 1)
        top = max(y1, labelSize[1])
        cv2.rectangle(frame, (x1 - 1, top - round(labelSize[1])), (x2+1, top ), COLOR_TABEL_OB[color_id1], cv2.FILLED)
        cv2.putText(frame, label, (x1, top), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, COLOR_BLACK, lineType=cv2.LINE_AA)

    return frame
