import cv2
# from detectmodel.SSD_Utils import LABELS
from detectmodel.Yolo_Utils import LABELS
# from Yolo_Utils import LABELS

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
# COLOR_TABEL_OB      = np.random.uniform(100, 255, size=(100, 3))
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

COLOR_TABEL_OB      = [COLOR_1, COLOR_2, COLOR_3, COLOR_4, COLOR_5, COLOR_6, COLOR_6]


def draw_object_predict(classes, probes, boxes, image) :
    (H, W) = image.shape[0:2]

    for index, (x, y, w, h) in enumerate(boxes) :
        xmin = max(0, x)
        ymin = max(0, y)
        xmax = min(xmin + w , W)
        ymax = min(ymin + h , H)
        label = "{}".format(LABELS[classes[index]], probes[index])
		# label = "{} : {:.2}".format(classes[index], probes[index])

        color = [int(c) for c in COLOR_TABEL_OB[classes[index]]]
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax),color, 2)

        labelSize, baseLine = cv2.getTextSize(label, cv2.FORMATTER_FMT_CSV, 0.75, 1)
        top = max(y, labelSize[1])
        cv2.rectangle(image, (x - 1, top - round(labelSize[1])), (x + w + 1, top ), color, cv2.FILLED)
        cv2.putText(image, label, (x, top), cv2.FORMATTER_FMT_CSV, 0.75, COLOR_BLACK, 1)

    return image
#
# Database configuration parameters
#

# Log mode


# -------------------------------------------------------------------------------
# Draw Line, pylogon in config
# -------------------------------------------------------------------------------

def draw_object_tracking2(frame, ObjectTracker,label_t, color_id1) :
    # 
    for object_track in ObjectTracker.currentObjects :
        color_id = int(str(object_track.objectID)[-2:])

        x, y, w, h = object_track.bbox

        ycenter = object_track.trace[-1][1]
        xcenter = object_track.trace[-1][0]
        
        cv2.circle(frame, (xcenter, ycenter), 7, COLOR_YELLOW, -1)
        cv2.rectangle(frame, (x, y), (x+w, y+h),COLOR_TABEL_OB[color_id1], 2)

        label = "{}".format(label_t)

        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, 1)
        top = max(y, labelSize[1])
        cv2.rectangle(frame, (x - 1, top - round(labelSize[1])), (x+w+1, top ), COLOR_TABEL_OB[color_id1], cv2.FILLED)
        cv2.putText(frame, label, (x, top), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, COLOR_BLACK, lineType=cv2.LINE_AA)

    #     text = "{}".format(object_track.objectID)

    #     cv2.putText(frame, text, (x + 20, y + 20),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TABEL_OB[color_id1], 2)
    

    
    # for object_track in ObjectTracker.hiddenObjects :
    #     color_id = int(str(object_track.objectID)[-2:])

    #     x, y, w, h = object_track.bbox

    #     ycenter = object_track.trace[-1][1]
    #     xcenter = object_track.trace[-1][0]
        
    #     cv2.circle(frame, (xcenter, ycenter), 7, COLOR_GREEN, -1)
    #     cv2.rectangle(frame, (x, y), (x+w, y+h),COLOR_TABEL_OB[color_id1], 2)

    #     label = "{}".format(label_t)

    #     labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, 1)
    #     top = max(y, labelSize[1])
    #     cv2.rectangle(frame, (x - 1, top - round(labelSize[1])), (x+w+1, top ), COLOR_TABEL_OB[color_id1], cv2.FILLED)
    #     cv2.putText(frame, label, (x, top), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, COLOR_BLACK, 1)

    #     text = "{}".format(object_track.objectID)

    #     cv2.putText(frame, text, (x + 20, y + 20),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TABEL_OB[color_id1], 2)
    
    # label = "Next ID : {}".format(str(ObjectTracker.nextObjectID)[-3:])
    # cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_YELLOW, 2)

    return frame
# -------------------------------------------------------------------------------
# Draw Line, pylogon in config
# -------------------------------------------------------------------------------

def draw_object_tracking(frame, ObjectTracker,label_t, color_id1) :    
    # 
    for object_track in ObjectTracker.currentObjects :
        color_id = int(str(object_track.objectID)[-2:])

        x, y, w, h = object_track.bbox

        ycenter = object_track.trace[-1][1]
        xcenter = object_track.trace[-1][0]
        
        cv2.circle(frame, (xcenter, ycenter), 7, COLOR_YELLOW, -1)
        cv2.rectangle(frame, (x, y), (x+w, y+h),COLOR_TABEL_OB[color_id1], 2)

        label = "{}".format(label_t)

        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, 1)
        top = max(y, labelSize[1])
        cv2.rectangle(frame, (x - 1, top - round(labelSize[1])), (x+w+1, top ), COLOR_TABEL_OB[color_id1], cv2.FILLED)
        cv2.putText(frame, label, (x, top), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, COLOR_BLACK, 1)

        # text = "{}".format(object_track.objectID)

        # cv2.putText(frame, text, (x + 20, y + 20),
        #         cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TABEL_OB[color_id1], 2)

    
    # for object_track in ObjectTracker.hiddenObjects :
    #     color_id = int(str(object_track.objectID)[-2:])

    #     x, y, w, h = object_track.bbox

    #     ycenter = object_track.trace[-1][1]
    #     xcenter = object_track.trace[-1][0]
        
    #     cv2.circle(frame, (xcenter, ycenter), 7, COLOR_YELLOW, -1)
    #     cv2.rectangle(frame, (x, y), (x+w, y+h),COLOR_TABEL_OB[color_id1], 2)

    #     label = "{}".format(label_t)

    #     labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, 1)
    #     top = max(y, labelSize[1])
    #     cv2.rectangle(frame, (x - 1, top - round(labelSize[1])), (x+w+1, top ), COLOR_TABEL_OB[color_id1], cv2.FILLED)
    #     cv2.putText(frame, label, (x, top), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, COLOR_BLACK, 1)

    #     text = "{}".format(object_track.objectID)

    #     cv2.putText(frame, text, (x + 20, y + 20),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TABEL_OB[color_id1], 2)
    
    # label = "Next ID : {}".format(str(ObjectTracker.nextObjectID)[-3:])
    # cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_YELLOW, 2)


    return frame



# -------------------------------------------------------------------------------
# Draw Line, pylogon in config
# -------------------------------------------------------------------------------

    