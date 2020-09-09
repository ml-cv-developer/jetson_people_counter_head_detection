'''
start a thread capture frames
save frames to redis server
'''
import sys
import traceback
from queue import Queue
from threading import Thread
import threading
import cv2
import logging
import datetime
import time
# sys.path.append('../')
from utils_ken.log.getlog import get_logger
log_cam       = get_logger(logname="cam", logfile='./logs/cam.log')

class FileVideoStream():
    '''
    Instance used to capture video's frames
    '''

    def __init__(self, cam_url, step=1):
        '''
        Initialize new object for capturing

        Args:
            cam_cfg -> dict:
            information of camera (camera id, camera address, process fps, ...)
        Return:
            None
        '''
        self.__cam_addr         = cam_url
        self.__step             = step
        self.__frame_queue      = Queue(maxsize=4)
        self.__stopped          = False
        self.last_frame         = False
        self.__stopped_lock     = threading.Lock()

        self.thread_c           = Thread(target=self.__update, args=())
        self.thread_c.daemon    = True        
        

    def start(self):
        '''
        Get the object started
        and create new thread to run

        Args:
            None
        Return:
            None
        '''
        log_cam.info("Start capture ... ")
        self.thread_c.start()
        return self

    def __update(self):
        '''
        Repeated grab new frame from Camera IP
        and run on another thread created before

        Args:
            None
        Return:
            None
        '''
        try:
            cnt = 0
            # capture or recapture
            capturer = cv2.VideoCapture(self.__cam_addr)

            while not self.get_stopped() :
            	# if not full queue, 
            	# read frame to queue, but not read all frame
                if not self.__frame_queue.full():
					# read frame
                    success, frame = capturer.read()
                    cnt +=1
                    # breack to recapture 
                    if not success :
                        time.sleep(1)
                        log_cam.info("Break file capture... ")
                        break
                	# Take a aframe to quue
                    if cnt >= self.__step:
                        # log_cam.info("queue put step {}".format(cnt))
                        self.__frame_queue.put(frame)
                        cnt = 0
                else :
                    # log_cam.info("queue is full, waiting ... ")
                    time.sleep(0.01)

            	#  log_cam.warning('Cam : {} break Reconnection '.format(self.__cam_id))
            while not self.__frame_queue.empty() :
                self.__frame_queue.get()
            
        
        except Exception as ex:
            traceback.print_exc()
            traceback.print_tb(ex.__traceback__)
            # capturer.release()
        finally:
            capturer.release()
            while not self.__frame_queue.empty():
                self.__frame_queue.get()

        log_cam.info('The end video file')
        self.last_frame         = True

    def stop(self):
        '''
        stop the camera thread
        '''
        self.__stopped_lock.acquire()
        self.__stopped = True
        self.__stopped_lock.release()
        while not self.__frame_queue.empty():
            self.__frame_queue.get()
        
        # self.thread_c.join()
        log_cam.warning("Cam terminateed ")


    def get_stopped(self):
        '''
        return true if thread need to stop, false if vice versa
        '''
        self.__stopped_lock.acquire()
        stopped = self.__stopped
        self.__stopped_lock.release()
        return stopped

    def is_lastframe(self):
        '''
        return true if thread need to stop, false if vice versa
        '''
        log_cam.info('last_frame is {}'.format(self.last_frame))
        last_frame = self.last_frame
        return last_frame

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
        # log_cam.info("queue is read ")
        return self.__frame_queue.get()
