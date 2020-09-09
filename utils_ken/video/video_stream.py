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


class VideoStream():
    '''
    Instance used to capture video's frames
    '''

    def __init__(self, cam_url, step=3):
        '''
        Initialize new object for capturing

        Args:
            cam_cfg -> dict:
            information of camera (camera id, camera address, process fps, ...)
        Return:
            None
        '''
        self.__cam_addr     = cam_url
        self.__step         = step
        self.__frame_queue  = Queue(maxsize=4)
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
                log_cam.info("Start capture video")
                capturer = cv.VideoCapture(self.__cam_addr)
                

                while not self.get_stopped() :
                    success, frame = capturer.read()
                    cnt +=1
                    if not success :
                        log_cam.info("break to recapture ")
                        time.sleep(10)
                        break
                    
                    if cnt >= self.__step:
                        # print(cnt)
                        if self.__frame_queue.full():
                            self.__frame_queue.get()
                            log_cam.info("queue full and waiting ")
                            time.sleep(0.1)
                        cnt = 0
                        log_cam.info("queue put ")
                        self.__frame_queue.put(frame)

                #  log_cam.info('Cam : {} break Reconnection '.format(self.__cam_id))
                while not self.__frame_queue.empty() :
                    self.__frame_queue.get()
                
            
            except Exception as ex:
                traceback.print_exc()
                traceback.print_tb(ex.__traceback__)
                log_cam.info("Cam lose connection")
                # capturer.release()
            finally:
                capturer.release()
                log_cam.info('Cam release Reconnection ')
                while not self.__frame_queue.empty():
                    self.__frame_queue.get()

        log_cam.info('Cam  is Stoped')
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

        # log_cam.info("Join Thread capture at at {}:{}".format(time_close.hour,time_close.minute))
        # self.thread_c.join()
        log_cam.info("Cam terminateed ")


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
        log_cam.info("queue get ")
        return self.__frame_queue.get()
