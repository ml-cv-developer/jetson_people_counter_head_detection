import os
import cv2
import time
import datetime
import numpy as np
from pascal_voc_writer import Writer as WriterXML
# from detectmodel.SSD_Utils import *
from detectmodel.Yolo_Utils import *

def save_image(frame,image_url, cam_cfg_id) :
    date_folder = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    ob_name     = "f_{}_{}".format(cam_cfg_id, date_folder)
    jpg_name    = "{}.jpg".format(ob_name)
    jpg_full    = os.path.join(image_url,jpg_name)
    cv2.imwrite(jpg_full, frame)
    # log_record.info("Save Image : {}".format(jpg_full))


def save_label_object(classes_id, rects, frame, camera_id, folderobject) :
    (H, W) = frame.shape[0:2]
    now = datetime.datetime.now()
        # date_folder = now.strftime('%Y-%m-%d')
    date_folder = now.strftime('%Y_%m_%d_%H_%M_%S')         
    current_minute  = datetime.datetime.now().minute
    ob_name = "f_{}_{}_{}".format(camera_id,date_folder,np.random.randint(100))
    xml_name = "{}.xml".format(ob_name)
    jpg_name = "{}.jpg".format(ob_name)
    print("save : {}".format(xml_name))
    xml_full = os.path.join(folderobject,xml_name)
    jpg_full = os.path.join(folderobject,jpg_name)

    writerXML = WriterXML(jpg_full,W, H)
    for index, (x,y, w, h) in enumerate(rects) :
        xmin = max(0, x) 
        ymin = max(0, y)
        xmax = min(x + w , W)
        ymax = min(y + h , H)
        
        label_ob = "{}".format(LABELS[classes_id[index]])
        writerXML.addObject(label_ob, xmin, ymin, xmax, ymax)
    
    # print(jpg_full)
    cv2.imwrite(jpg_full, frame)
    writerXML.save(xml_full)


