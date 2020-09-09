import os
import cv2 
import numpy as np 
import datetime
from utils_ken.log.getlog import get_logger
"""
    This class will save small video at event have object action
    
"""
# ID for human

log_video      = get_logger('video_write','./logs/video_write.log')


class SaveVideoHour : 
    def __init__(self,url_folder, cam_id, No_Frame_Flow=60*15*20) :
        self.cam_id            = cam_id
        self.url            = url_folder
        self._write         = None
        self.No_Frame_Flow  = No_Frame_Flow
        self.writing        = False
        self.counterSkip    = 0
        self.hour_record    = -1
        

    def __create_writer(self) :
        now = datetime.datetime.now()
        # date_folder = now.strftime('%Y-%m-%d')
        date_folder = now.strftime('%Y_%m_%d_%H_%M_%S')

        # Name folder video
        # folder_save         = os.path.join(head_folder,date_folder)
        folder_save         = self.url
        self.hour_record    = now.hour
        # video_name          = 'cam_{}_{}.avi'.format(date_folder,self.cam_id,np.random.randint(100))
        video_name          = '{}_cam_{}.avi'.format(date_folder,self.cam_id)
        self.video_url           = os.path.join(folder_save, video_name)
        log_video.info("Create video : {}".format(self.video_url))
        if not os.path.exists(folder_save) :
            log_video.info("os.makedirs : {}".format(folder_save))
            os.makedirs(folder_save)
        

        #  for save small size
        fourcc = cv2.VideoWriter_fourcc(*"XVID") 
        #  for save youtube live

        # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(self.video_url, fourcc, 15,(1280, 720), True)
        return writer

    def update(self, frame) :
        current_hour = datetime.datetime.now().hour
        frame = cv2.resize(frame, (1280, 720))

        if self.writing is False and current_hour != self.hour_record :
            self.writing = True

        if self.writing is True :
            if self._write is None : 
                self._write         = self.__create_writer()
                self._write.write(frame)
                self.counterSkip    = 0
        
            if self._write is not None :
                # frame = cv2.resize(frame, (1280, 720))
                self._write.write(frame) 
                self.counterSkip += 1

                # if self.counterSkip >= self.No_Frame_Flow :
                if current_hour != self.hour_record :
                    self._write.release()
                    log_video.info("release video ")
                    # post_video(self.video_url)
                    self.writing    = False
                    self._write     = None 


def run() :
    url = 'rtsp://user1:123456a@@374xd.vncctv.info//cam/realmonitor?channel=3&subtype=0'
    video_5minute       = '/home/ken/workspace/nano_package/video_5minute'
    write       = SaveVideoHour(video_5minute)
    video_cap   = cv2.VideoCapture(url)

    while True :
        _,frame = video_cap.read()
        write.update(frame)

if __name__  =='__main__' :
    run()