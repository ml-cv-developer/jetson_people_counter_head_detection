import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from utils_machine import videos_output
from utils_machine import images_output

from trackmodel.centroidRecognize import RdfTracker
from threading import Thread
from queue import Queue
import datetime
from utils_ken.log.getlog import get_logger
from utils_ken.video.recapvideostream import RecapVideoStream
from utils.utils_mode_counter import POLYGON_FILTER
from utils.utils_mode_counter import COUNTER_ONEWAY_IDS
from utils.utils_mode_counter import POLYGON_COUNTER_IDS

from utils.utils_save_video import SaveVideoHour
from utils.utils_color import *
from utils.utils_color import draw_object_tracking2

from utils.utils_polygon import draw_polygon
from utils.utils_polygon import utils_popygon

from utils_excel.utils_excel_sum_hour import export_excel
from display.draw_table_display import draw_table_display


from utils.utils_counter import Counter_Line2Way

from utils.utils_label_xml import save_image

from ubidots.utils_ubidots import Api_Ubidots

from utils.utils_counter import Counter_Polygon

from light.lightapi import ApiLight

from detectmodel.tf_detector import TfDetector
from detectmodel.tracker import Tracker
from detectmodel.setting import *
from detectmodel import func


logcore         = get_logger('core','./logs/core.log')


if not os.path.exists(videos_output) :
    logcore.info("os.makedirs : {}".format(videos_output))
    os.makedirs(videos_output)

if not os.path.exists(images_output) :
    logcore.info("os.makedirs : {}".format(images_output))
    os.makedirs(images_output)


sent_db             = False


class Core():

    def __init__(self, conf, camCfg, lockDetect, frame_out):
        '''
            Initilize model and specify video source
        '''

        self.detector_lock = lockDetect
        self.__camCfg = camCfg
        print(self.__camCfg)
        self.List_object = conf['vehicle_type']
        self.conf = conf

        self.model = TfDetector()
        self.tracker = Tracker()
        self.total_in = 0
        self.total_out = 0

        line_p1 = np.array(self.__camCfg['funcs'][1]['func_line'][:2])
        line_p2 = np.array(self.__camCfg['funcs'][1]['func_line'][2:])
        p3 = np.array(self.__camCfg['funcs'][1]['func_pont'][:2])
        p4 = np.array(self.__camCfg['funcs'][1]['func_pont'][2:])
        d1 = func.get_distance_from_line(line_p1, line_p2, p3)
        d2 = func.get_distance_from_line(line_p1, line_p2, p4)
        if d1 < 0 and d2 > 0:
            self.direction = True
        else:
            self.direction = False

        self.tracker_object = RdfTracker(maxObjectTrack=self.conf["maxObjectTrack"], maxDistance=self.conf["maxDistance"], maxTrace=5, max_Timedisappeared = self.conf["max_Timedisappeared"])

        self.frame_out  = frame_out
        # self.lock               = lock

        self.__queue_frame      = Queue(maxsize=4)
        self.__queue_predict    = Queue(maxsize=4)

        self.thread_prec        = Thread(target=self.__predict)
        self.thread_prec.daemon = True
        self.thread_prec.start()

        # self.__cap = CameraCapture(self.__camCfg)
        self.__cap = RecapVideoStream(self.__camCfg)
        # self.__cap = FileVideoStream(self.__camCfg['cam_Link'], step=1)

        if self.conf["send_ubidot"] :
            self.api_ubidot = Api_Ubidots(self.conf)

        if self.conf['light_api'] :
            self.light_api = ApiLight(self.conf)

    def check_valid_detection(self, rect_list, score_list, class_list):
        check_rect_list = []
        check_score_list = []

        # ----------------------- check validation using threshold and ROI ------------------------
        for i in range(len(score_list)):
            if class_list[i] != 1 or score_list[i] < DETECTION_THRESHOLD:
                continue

            # check ROI
            roi = self.__camCfg['funcs'][0]['func_note']
            if rect_list[i][0] + rect_list[i][2] < roi[0][0] * 2:
                continue
            elif rect_list[i][0] + rect_list[i][2] > roi[1][0] * 2:
                continue
            elif rect_list[i][1] + rect_list[i][3] < roi[0][1] * 2:
                continue
            elif rect_list[i][1] + rect_list[i][3] > roi[2][1] * 2:
                continue

            # check overlap with other rects
            f_overlap = False
            for j in range(len(check_rect_list)):
                if func.check_overlap_rect(check_rect_list[j], rect_list[i]):
                    if check_score_list[j] < score_list[i]:
                        check_score_list[j] = score_list[i]
                        check_rect_list[j] = rect_list[i]
                    f_overlap = True
                    break

            if f_overlap:
                continue

            # check width/height rate
            w = rect_list[i][2] - rect_list[i][0]
            h = rect_list[i][3] - rect_list[i][1]
            if max(w, h) / min(w, h) > 2:
                continue

            # register data
            check_rect_list.append(rect_list[i])
            check_score_list.append(score_list[i])

        # ------------ check validation by check body and calculate distance from cross line ------
        final_rect = []
        final_score = []
        final_distance = []

        line_p1 = np.array(self.__camCfg['funcs'][1]['func_line'][:2])
        line_p2 = np.array(self.__camCfg['funcs'][1]['func_line'][2:])

        for i in range(len(check_rect_list)):
            r_body = check_rect_list[i]
            body_h = r_body[3] - r_body[1]
            body_w = r_body[2] - r_body[0]
            f_ignore = False
            for j in range(len(check_rect_list)):
                r2 = check_rect_list[j]
                if r_body[0] < (r2[0] + r2[2]) / 2 < r_body[2] or r2[0] < (r_body[0] + r_body[2]) / 2 < r2[2]:
                    if abs(r_body[1] - r2[3]) * 1.5 < r2[3] - r2[1] and r_body[3] > r2[3] + 0.5 * (r2[3] - r2[1]):
                        if body_h > 1.2 * (r2[3] - r2[1]) or body_w > 1.2 * (r2[2] - r2[0]):
                            f_ignore = True
                            break

            if not f_ignore:
                final_rect.append(check_rect_list[i])
                final_score.append(check_score_list[i])

                p3 = np.array([(check_rect_list[i][0] + check_rect_list[i][2]) / 2,
                               (check_rect_list[i][1] + check_rect_list[i][3]) / 2])
                final_distance.append(func.get_distance_from_line(line_p1, line_p2, p3))

        return final_rect, final_score, final_distance

    def detect_frame(self, img):
        roi = self.__camCfg['funcs'][0]['func_note']
        roi = [max(0, roi[0][0] - 20),
               max(0, roi[0][1] - 20),
               min(960, roi[1][0] + 20),
               min(540, roi[2][1] + 20)]

        img_crop = img[roi[1]:roi[3], roi[0]:roi[2]]
        det_rect_list, det_score_list, det_class_list = self.model.detect_from_images(img_crop)
        for i in range(len(det_rect_list)):
            det_rect_list[i][0] += roi[0]
            det_rect_list[i][1] += roi[1]
            det_rect_list[i][2] += roi[0]
            det_rect_list[i][3] += roi[1]

        return det_rect_list, det_score_list, det_class_list

    def __predict(self):
        """
            Model Detect predict frame in thread
            Args :
                None
            return :
                None
        """
        frame_ind = 0
        while True:
            if not self.__queue_frame.empty():
                frame_ind += 1
                frame = self.__queue_frame.get()
                self.detector_lock.acquire()
                rects, probs, classesID = self.detect_frame(frame)
                valid_rects, valid_scores, valid_distances = self.check_valid_detection(rects, probs, classesID)

                cnt_in, cnt_out = self.tracker.update(frame_ind, valid_rects, valid_distances)
                if self.direction:
                    self.total_in += cnt_in
                    self.total_out += cnt_out
                else:
                    self.total_in += cnt_out
                    self.total_out += cnt_in

                self.detector_lock.release()
                self.__queue_predict.put((valid_rects, valid_scores, valid_distances, frame))

    def disconnect(self):
        pass

    def process(self, show_video=True):
        '''
            Detect human from Video source by loaded model
        '''
        logcore.info('Cam- {:0>4} starting ...'.format(self.__camCfg['cam_ID']))

        if self.conf['video_mode']:
            video_writer                        = SaveVideoHour(videos_output, self.__camCfg['cam_ID'])
            # video_writer_org                    = SaveVideoHour(videos_output, self.__camCfg['cam_ID'])

        if self.conf['save_excel']:
            now = datetime.datetime.now()
            # date_folder = now.strftime('%Y-%m-%d_%H_%M')
            date_folder = now.strftime('%Y-%m-%d')

            cam_ID = self.__camCfg['cam_ID']
            cam_Name = self.__camCfg['cam_Name']
            excel_file = "{}/{}_{}.xlsx".format(self.conf['excels_output'], cam_Name, date_folder)
            self.excel_report = export_excel(excel_file, cam_ID, cam_Name)
            logcore.info('excel_file {}'.format(excel_file))

        # check function model run
        cam_funcs = []

        for index, func in enumerate(self.__camCfg["funcs"]):

            if func["func_ID"] in COUNTER_ONEWAY_IDS :

                line_func                   = {}
                line_func['id']             = int(func["func_ID"])
                line_func['func_Name']        = func["func_Name"]
                # line, points                = decode_note_counter_line(func["func_note"])
                line                        = func['func_line']
                points                      = func['func_pont']
                line_func["points"]         = line
                line_func["points2"]        = points

                line_func[0]    = Counter_Line2Way(line, points)


                cam_funcs.append(line_func)
                # ----------------------------------------------------------------------------------------------------
                if self.conf['save_excel'] is True :
                    sheet_line_name                = "{}_line_id{}".format(self.__camCfg['cam_ID'], func["func_Name"])
                    logcore.info('create_sheet : {}'.format(sheet_line_name))
                    self.excel_report.create_sheet(sheet_line_name,  func["func_ID"], func["func_Name"])
                # ----------------------------------------------------------------------------------------------------

                logcore.info("line_func['id']  : {}".format(line_func['id']))

            if func["func_ID"] in POLYGON_COUNTER_IDS :

                counter_func                   = {}
                counter_func['id']             = func["func_ID"]
                counter_func['func_Name']        = func["func_Name"]
                coords                         = func["func_note"]
                counter_func["func_Name"]      = func["func_Name"]
                counter_func["coords"]         = coords

                counter_func[0]    = Counter_Polygon(coords)

                cam_funcs.append(counter_func)
                logcore.info("line_func['id']  : {}".format(counter_func['id']))

                # ----------------------------------------------------------------------------------------------------
                if self.conf['save_excel'] is True :
                    sheet_polygon_name          = "{}_zone_{}".format(self.__camCfg['cam_ID'],func["func_Name"])
                    logcore.info('create_sheet : {}'.format(sheet_polygon_name))
                    self.excel_report.create_sheet(sheet_polygon_name,  func["func_ID"], func["func_Name"])
                # ----------------------------------------------------------------------------------------------------

            if func["func_ID"] == POLYGON_FILTER :
                polygon_func = {}
                polygon_func['id']      = POLYGON_FILTER
                # polygon_func["coords"]  = decode_note_polygon(func["func_note"])
                polygon_func["coords"]  = func["func_note"]
                polygon_func["filter"]  = utils_popygon(polygon_func["coords"])

                cam_funcs.append(polygon_func)

        minute_write_xml            = datetime.datetime.now().minute
        minute_send_data_keep       = datetime.datetime.now().minute
        minute_counter              = datetime.datetime.now().minute
        pre_day                     = datetime.datetime.now().day
        pre_hour                    = datetime.datetime.now().hour

        count_frame_process         = 0

        self.__cap.start()

        while True:
            frame = self.__cap.read()
            if not self.__queue_frame.full() and  frame is not None:
                # frame = cv2.resize(frame, (1280,720) )
                frame = cv2.resize(frame, (960, 540))
                self.__queue_frame.put(frame)

            if frame is None :
                logcore.info("frame is None ")

            # predict and processing tracking
            if not self.__queue_predict.empty() :
                # Get predict detection
                # logcore.warning('----- track ------------------')
                (boxes, probs, distances, frame_pre) = self.__queue_predict.get()

                frame_ori = frame_pre.copy()
                count_frame_process +=1
                # Get predict detection
                # -----------------------------------------------------------------------------------------------------------
                probs_data = probs
                if self.conf['images_mode'] is True :
                    current_minute = datetime.datetime.now().minute
                    if len(probs_data) >= 1 and current_minute != minute_write_xml and current_minute % self.conf["take_every"] ==0:
                        logcore.info("write image : {}".format(current_minute))

                        # save_label_object(classesID, boxes, frame_ori, self.__camCfg["cam_ID"], folderobject)
                        save_image(frame_ori, images_output, self.__camCfg["cam_ID"])
                        minute_write_xml = current_minute

                # -----------------------------------------------------------------------------------------------------------
                for cam_func in cam_funcs :
                    if cam_func['id'] == POLYGON_FILTER :
                        # classesID, probs, boxes = cam_func["filter"].filter_ob(classesID, probs, boxes)
                        draw_polygon(frame_pre,cam_func['coords'])

                # classification object and tracking
                self.tracker_object.update(boxes, frame_pre)

                # classification counting object for many line

                for cam_func in cam_funcs :
                    if cam_func['id'] in COUNTER_ONEWAY_IDS :
                        light_trackid, light_aciton = cam_func[0].update(self.tracker_object.currentObjects)

                if self.conf['light_api'] :
                    if len(light_trackid) > 0 :
                        for index_id, track_id in enumerate(light_trackid) :
                            self.light_api.send_action(light_trackid[index_id], light_aciton[index_id])

                draw_table_display(cam_funcs, frame_pre, self.total_in, self.total_out)
                # -------------------------------------------------------------------------------
                # Test counter line
                # Draw object, erea
                # -------------------------------------------------------------------------------

                frame_pre = draw_object_tracking2(frame=frame_pre,ObjectTracker=self.tracker_object,label_t='person', color_id1=0)

                if self.conf['video_mode'] :
                    video_writer.update(frame_pre)

                if 'DISPLAY' in os.environ and  self.conf['show_video']:
                    cv2.imshow("Video {}".format(self.__camCfg["cam_ID"]),frame_pre)
                    k = cv2.waitKey(1) & 0xff
                    if k == ord('q') :
                        break

                # with self.lock :
                if self.frame_out.full() :
                    self.frame_out.get()
                    self.frame_out.put(frame_pre.copy())
                else:
                    self.frame_out.put(frame_pre.copy())

            # ---------------------------------------------------------------------------------------
            minute_send_data = datetime.datetime.now().minute
            if minute_send_data_keep  != minute_send_data and minute_send_data % self.conf["updated_every"] ==0:
                minute_send_data_keep  = minute_send_data

                logcore.info("Update traffic log, static, excel : {}".format(minute_send_data_keep))

                for cam_func in cam_funcs :
                    if cam_func['id'] in COUNTER_ONEWAY_IDS :

                        data_send = {}
                        data_send['camera_id'] = self.__camCfg['cam_ID']
                        list_up_counter     = []
                        list_down_counter   = []
                        list_sum            = []

                        cnt_up = self.total_in
                        cnt_down = self.total_out
                        self.total_in = 0
                        self.total_out = 0

                        # cnt_up, cnt_down    = cam_func[0].get_counter_and_clean()

                        data_send[0] = cnt_up + cnt_down

                        list_up_counter.append(cnt_up)
                        list_down_counter.append(cnt_down)
                        list_sum.append(cnt_up + cnt_down)

                        # if sent_db is True:
                            # SEND database_api
                            # self.database_api.send(data_send)
                        if self.conf['save_excel'] is True :
                            sheet_line_name                = "{}_line_id{}".format(self.__camCfg['cam_ID'], cam_func["func_Name"])
                            self.excel_report.update_line(sheet_line_name, list_up_counter, list_down_counter)
                            self.excel_report.save()

                        if self.conf["send_ubidot"] :
                            self.api_ubidot.send_up_traffic(*list_up_counter)
                            self.api_ubidot.send_down_traffic(*list_down_counter)
                            self.api_ubidot.send_sum_traffic(*list_sum)

                    if cam_func['id'] in POLYGON_COUNTER_IDS :

                        data_send = {}
                        data_send['camera_id'] = self.__camCfg['cam_ID']
                        list_counter     = []
                        for index, obiect_index in enumerate(self.List_object) :
                            counter_no    = cam_func[obiect_index].get_counter_and_clean()

                            data_send[obiect_index] = counter_no

                            list_counter.append(counter_no)

                        # if sent_db is True:
                            # SEND database_api
                            # self.database_api.send(data_send)
                        if self.conf['save_excel'] is True :
                            sheet_polygon_name          = "{}_zone_{}".format(self.__camCfg['cam_ID'], cam_func["func_Name"])

                            self.excel_report.update_polygon(sheet_polygon_name, list_counter)
                            self.excel_report.save()

                        if self.conf["send_ubidot"] :
                            # self.api_ubidot.send_sum_traffic(*list_counter)
                            self.api_ubidot.send_zone_traffic(*list_counter)

            # ---------------------------------------------------------------------------------------
            #  write excel every five minute
            # ---------------------------------------------------------------------------------------
            minute_send_data = datetime.datetime.now().minute
            if minute_counter  != minute_send_data :
                minute_counter  = minute_send_data
                logcore.info("minute  {} Cam {} processing {} Frame".format(minute_counter, self.__camCfg['cam_ID'], count_frame_process))
                count_frame_process = 0

            current_hour = datetime.datetime.now().hour
            current_day = datetime.datetime.now().day
            if current_day != pre_day :
                pre_day     = current_day
                logcore.info("reset counter per day : {} ".format(current_day))

                # -----------------------------------------------------------------------------------------
                if self.conf['save_excel'] is True :
                    now = datetime.datetime.now()
                    # date_folder = now.strftime('%Y-%m-%d_%H_%M')
                    date_folder = now.strftime('%Y-%m-%d')

                    cam_ID          = self.__camCfg['cam_ID']
                    cam_Name        = self.__camCfg['cam_Name']
                    excel_file      = "{}/{}_{}.xlsx".format(self.conf['excels_output'], cam_Name,date_folder)
                    self.excel_report    = export_excel(excel_file, cam_ID, cam_Name)
                    logcore.info('excel_file {}'.format(excel_file))
                # -----------------------------------------------------------------------------------------

                for index, func  in enumerate(self.__camCfg["funcs"]) :

                    if func["func_ID"] in COUNTER_ONEWAY_IDS :
                        if self.conf['save_excel'] is True :
                            sheet_line_name                = "{}_line_id{}".format(self.__camCfg['cam_ID'], func["func_Name"])
                            logcore.info('create_sheet : {}'.format(sheet_line_name))
                            self.excel_report.create_sheet(sheet_line_name,  func["func_ID"], func["func_Name"])

                    if func["func_ID"] in POLYGON_COUNTER_IDS :
                        if self.conf['save_excel'] is True :
                            sheet_polygon_name          = "{}_zone_{}".format(self.__camCfg['cam_ID'],func["func_Name"])
                            logcore.info('create_sheet : {}'.format(sheet_polygon_name))
                            self.excel_report.create_sheet(sheet_polygon_name,  func["func_ID"], func["func_Name"])


            # pre_minute      = current_minute
            pre_hour        = current_hour
            pre_day         = current_day
            # logcore.warning('---------------- one round ------------------')

        logcore.warning('---------------- Exception 2 ------------------')

    def close(self):
        '''
            Clean resources and terminate service
        '''
        self.__del__()
        time_close = datetime.datetime.now()
        logcore.warning("Cam- {} closeed at {}:{}".format(self.__camCfg['cam_ID'],time_close.hour,time_close.minute))

    def __del__(self):
        self.__cap.stop()
        logcore.info('Cleaning resources...\n')
