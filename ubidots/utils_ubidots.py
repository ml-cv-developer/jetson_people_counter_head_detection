import time
import requests
import math
import random
import numpy as np
import threading
import datetime
from utils_ken.log.getlog import get_logger

from utils import Conf



logubidot_line         = get_logger('ubidot','./logs/ubidot.log')


class Api_Ubidots() :
    def __init__(self, conf) :
        self.conf = conf
        self.token, self.machine, self.lat, self.lng = self.gettoken(self.conf) 
        # -------------------------------------------
        if self.lat is not None and self.lng is not None :
            self.send_postition(self.lat, self.lng)

    # -----------------------------------------------------------------------------------
    # decode json to get token
    def gettoken(self, conf) : 
        # data_configs  = Conf(conf)

        token   = conf['ubidot_token']
        machine = conf['machine']


        lat     = conf['lat']
        lng     = conf['lng']

        if token is None or machine is None :
            raise "ubidot error information"
        

        return token, machine, lat, lng

    # -----------------------------------------------------------------------------------
    def build_payload_position(self, lat, lng) :
        payload = {     "position"  : {"value": 1, "context": {"lat": lat, "lng": lng}}
                }
        return payload   
    # -----------------------------------------------------------------------------------
    def build_payload_up(self, person) :
        payload = {     "person_up_raw"  : person
                }

        return payload


    # -----------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------
    def build_payload_down(self, person) :
        payload = {     "person_down_raw"  : person
                }
        return payload 


    def build_payload_sum(self, person) :
        payload = {     
                    "person_raw"  : person
                }
        return payload        

    # -----------------------------------------------------------------------------------
    def post_request(self, payload):
        # Creates the headers for the HTTP requests
        url = "http://things.ubidots.com"
        url = "{}/api/v1.6/devices/{}".format(url, self.machine)
        headers = {"X-Auth-Token": self.token, "Content-Type": "application/json"}

        # Makes the HTTP requests
        status = 400
        attempts = 0
        while status >= 400 and attempts <= 5:
            req = requests.post(url=url, headers=headers, json=payload)
            status = req.status_code
            attempts += 1
            time.sleep(5)

        # Processes results
        if status >= 400:
            logubidot_line.info("[ERROR] Could not send data after 5 attempts, please check \
                your token credentials and internet connection")
            return False

        # logubidot_line.info("[INFO] request made properly, your device is updated")
        return True


    def _send_postition(self, lat, lng):
        payload = self.build_payload_position(lat, lng)
        self.post_request(payload)


    def _send_up_traffic(self, person ):
        payload = self.build_payload_up(person )
        self.post_request(payload)

    def _send_down_traffic(self, person):
        payload = self.build_payload_down(person)
        self.post_request(payload)


    def _send_sum_traffic(self, person):
        payload = self.build_payload_sum(person)
        self.post_request(payload)


    def send_up_traffic(self, person ):
        logubidot_line.info("send count up {}".format([person]))
        thread = threading.Thread(target=self._send_up_traffic, args=(person,))
        # thread.daemon = True
        thread.start()        


    def send_down_traffic(self, person ):
        logubidot_line.info("send count down {}".format([person]))
        thread = threading.Thread(target=self._send_down_traffic, args=(person,))
        # thread.daemon = True
        thread.start()        



    def send_sum_traffic(self, person ):
        logubidot_line.info("send count sum {}".format([person]))
        thread = threading.Thread(target=self._send_sum_traffic, args=(person,))
        # thread.daemon = True
        thread.start()        


    def  send_postition(self, lat, lng):
        logubidot_line.info("send position {}".format([lat, lng]))
        thread = threading.Thread(target=self._send_postition, args=(lat, lng,))
        # thread.daemon = True
        thread.start()        



def main():
    logubidot_line.info(" =========================================")

    people_count    = np.random.randint(20, 25) 
    bikebike_count  = np.random.randint(20, 30) 
    car_count       = np.random.randint(100, 150)
    truck_count     = np.random.randint(30, 50)
    bus_count       = np.random.randint(30, 60)
    # init data accessor
    
    send_up_traffic(DEVICE_LABEL, people_count, id_line)
    send_down_traffic(DEVICE_LABEL,people_count, id_line)

if __name__ == '__main__':

    # read database config
    main()
    
    pre_minute =  datetime.datetime.now().minute
    while True:

        curent_minute =  datetime.datetime.now().minute
        if pre_minute != curent_minute and curent_minute %15 == 1:

            main()
            pre_minute = curent_minute
            logubidot_line.info("update at :{}".format(curent_minute))
