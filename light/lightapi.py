import time
import requests
import math
import random
import numpy as np
import threading
import datetime
from utils_ken.log.getlog import get_logger

from utils import Conf



light         = get_logger('light','./logs/light.log')


class ApiLight() :
    def __init__(self, conf) :
        self.conf = conf
        self.place_id, self.ip_machine = self.get_info(self.conf) 
        # -------------------------------------------

    # -----------------------------------------------------------------------------------
    # decode json to get place_id
    def get_info(self, conf) : 
        # data_configs  = Conf(conf)

        place_id   = conf['placeId']
        ip_machine = conf['ip_machine']

        if place_id is None or ip_machine is None :
            raise "place_id or ip_machine error information"

        return place_id, ip_machine
    # -----------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------

    def _send_action(self, trackingId, actionName):
        # Creates the headers for the HTTP requests
        url1 = 'https://{}/person?placeId={}&trackingId={}'.format(self.ip_machine, self.place_id,trackingId)
        light.info('url {}'.format(url1))
        # Makes the HTTP requests
        status = 400
        attempts = 0
        while status >= 400 and attempts <= 5:
            req = requests.post(url1,verify=False)
            print(req)
            status = req.status_code
            person_id = req.json()['personId']
            light.info('personId {}'.format(person_id))
            attempts += 1
            time.sleep(5)

        if status == 200 :
            status = 400
            attempts = 0
            url2 = 'https://{}/person/action?personId={}&actionName={}'.format(self.ip_machine, person_id, actionName)
            light.info('url {}'.format(url2))
            while status >= 400 and attempts <= 5:
                req = requests.post(url2,verify=False)
                print(req)
                status = req.status_code
                person_id = req.json()['personActionId']
                light.info('personActionId {}'.format(person_id))

                attempts += 1
                time.sleep(5)
                
        # Processes results
        if status >= 400:
            light.info("[ERROR] Could not send data after 5 attempts, please check \
                your token credentials and internet connection")
            return False

        # light.info("[INFO] request made properly, your device is updated")
        return True



    def send_action(self, trackingId, actionName ):
        light.info("send trackingId {} {} ".format(trackingId, actionName))
        thread = threading.Thread(target=self._send_action, args=(trackingId, actionName,))
        thread.daemon = True
        thread.start()        




if __name__ == '__main__':

    config_server = '../jetson/configs.json'
    conf = Conf(config_server)

    light_api = ApiLight(conf)

    light_api.send_action(123,"out")