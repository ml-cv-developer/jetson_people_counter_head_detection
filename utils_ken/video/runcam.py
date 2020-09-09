import json
import cv2
from recapvideostream import RecapVideoStream

def main(cam_cfg) :
    cam_cfg["step"] = 2
    caps = RecapVideoStream(cam_cfg)
    caps.start()
    while True:
        frame = caps.get_frame()
        cv2.imshow("frame", frame)
        k = cv2.waitKey(1) & 0xff
        if k == ord('q') :
            break
    caps.terminate()


if __name__ =='__main__' :
    with open("config.json") as f :
        cfgs = json.load(f)
    cam_cfgs = cfgs['list_cam']
    for i in range(len(cam_cfgs)) :
        main(cam_cfgs[i])