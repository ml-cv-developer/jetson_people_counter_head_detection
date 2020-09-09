import numpy as np
import cv2
from utils.utils_mode_counter import COUNTER_ONEWAY_IDS


from utils.utils_draw_2way import draw_no_object as draw_no_object_line


def draw_table_display(cam_funcs, frame_pre, cnt_up, cnt_down) :

     index1 = 0
     for cam_func in cam_funcs :
          if cam_func['id'] in COUNTER_ONEWAY_IDS :
               wimg = 50 + 40
               himg = 500
               img = np.zeros((wimg,himg,3), np.uint8)

               draw_no_object_line(img, "person", cnt_up, cnt_down, 0)
               cv2.line(frame_pre, tuple(cam_func["points"][:2]),tuple(cam_func["points"][2:]), (255, 0, 255), 2)
               cv2.arrowedLine(frame_pre,tuple(cam_func["points2"][:2]),tuple(cam_func["points2"][2:]), (255, 0, 255), 3, cv2.LINE_AA,0, tipLength = 0.05)

               img = cv2.resize(img,(himg//2,wimg//2))
               x_start = 10
               y_start = 10 + index1 * (wimg //2 + 10)

               frame_pre1      = cv2.addWeighted(frame_pre[y_start : wimg//2+y_start,x_start : himg//2+x_start,:],0.1,img,0.9,0)

               frame_pre[y_start:wimg//2+y_start, x_start:himg//2+x_start,:] = frame_pre1

               index1 +=1
