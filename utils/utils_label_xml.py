import os
import cv2
import time
import datetime
import numpy as np

def save_image(frame,image_url, cam_cfg_id) :
    date_folder = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    ob_name     = "f_{}_{}".format(cam_cfg_id, date_folder)
    jpg_name    = "{}.jpg".format(ob_name)
    jpg_full    = os.path.join(image_url,jpg_name)
    cv2.imwrite(jpg_full, frame)
    # log_record.info("Save Image : {}".format(jpg_full))



