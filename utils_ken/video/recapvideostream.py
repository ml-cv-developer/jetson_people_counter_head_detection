'''
start a thread capture frames
save frames to redis server
'''
import sys
import traceback
from queue import Queue
from threading import Thread
import threading
import cv2 as cv
import logging
import datetime
import time
# sys.path.append('../')
from utils_ken.log.getlog import get_logger
log_cam       = get_logger(logname="cam", logfile='./logs/cam.log')

class RecapVideoStream():
    '''
    Instance used to capture video's frames
    '''

    def __init__(self, cam_cfg):
        '''
        Initialize new object for capturing

        Args:
            cam_cfg -> dict:
            information of camera (camera id, camera address, process fps, ...)
        Return:
            None
        '''
        self.__cam_addr     = cam_cfg['cam_Link']
        self.__cam_id       = cam_cfg['cam_ID']
        self.__step         = cam_cfg['step']
        self.__frame_queue  = Queue(maxsize=1)
        self.__stopped      = False
        
        self.__stopped_lock = threading.Lock()
        

    def start(self):
        '''
        Get the object started
        and create new thread to run

        Args:
            None
        Return:
            None
        '''
        self.thread_c          = Thread(target=self.__update, args=())
        self.thread_c.daemon   = True
        self.thread_c.start()
        # return self

    def __update(self):
        '''
        Repeated grab new frame from Camera IP
        and run on another thread created before

        Args:
            None
        Return:
            None
        '''
        while not self.get_stopped():
            try:
                cnt = 0
                # capture or recapture
                capturer = cv.VideoCapture(self.__cam_addr)
                log_cam.info("Cam : {} start capture video ... ".format(self.__cam_id))

                while not self.get_stopped() :
                    success, frame = capturer.read()
                    cnt +=1
                    if not success :
                        log_cam.info("Cam : {} Read not success ".format(self.__cam_id))
                        time.sleep(10)
                        break
                    
                    if cnt >= self.__step:
                        # print(cnt)
                        # log_cam.warning("put frame at  {}".format(cnt)) 
                        if self.__frame_queue.full():
                            self.__frame_queue.get()
                            # log_cam.warning("Cam : {} Full".format(self.__cam_id)) 
                        cnt = 0
                        self.__frame_queue.put(frame)

                    time.sleep(0.01)

                log_cam.warning('Cam : {} break Reconnection '.format(self.__cam_id))
                while not self.__frame_queue.empty() :
                    self.__frame_queue.get()
                
            
            except Exception as ex:
                traceback.print_exc()
                traceback.print_tb(ex.__traceback__)
                log_cam.warning("Cam : {} Lose connection".format(self.__cam_id))
                # capturer.release()
            finally:
                capturer.release()
                log_cam.warning('Cam : {} release Reconnection '.format(self.__cam_id))
                while not self.__frame_queue.empty():
                    self.__frame_queue.get()

        log_cam.info('Cam : {} is Stoped '.format(self.__cam_id))
    def stop(self):
        '''
        stop the camera thread
        '''
        self.__stopped_lock.acquire()
        self.__stopped = True
        self.__stopped_lock.release()
        while not self.__frame_queue.empty():
            self.__frame_queue.get()
        
        time_close = datetime.datetime.now()

        # log_cam.warning("Join Thread capture at at {}:{}".format(time_close.hour,time_close.minute))
        # self.thread_c.join()
        log_cam.warning("Cam : {} terminateed at {}:{}".format(self.__cam_id,time_close.hour,time_close.minute))


    def get_stopped(self):
        '''
        return true if thread need to stop, false if vice versa
        '''
        self.__stopped_lock.acquire()
        stopped = self.__stopped
        self.__stopped_lock.release()
        return stopped

    def read(self):
        '''
        Read a frame from Queue and return
        Args:
            None
        Return:
        frame -> np.array((H, W, 3) ):
                frame from Camera if available
                otherwise None
        '''
        # if self.__frame_queue.empty() :
        #     return None
        # else :
        return self.__frame_queue.get()

    def get_cam_id(self):
        '''
        return id of camera
        Args:
            None
        Return:
            an integer that is the camera id
        '''
        return self.__cam_id
