import os
import json
from utils_ken.log.getlog import get_logger

from core.Core_theard import Core
from flask import Response
from flask import Flask
from flask import render_template

import threading

from utils import Conf


from queue import Queue

from utils.utils_polygon import decode_note_counter
from utils.utils_polygon import decode_note_polygon


from flask import request
from flask import redirect
from flask import url_for
from flask import session
from datetime import timedelta
import time
import cv2



logruncv = get_logger('watchdog','./logs/watchdog.log')

# initialize a flask object
app = Flask(__name__)
app.secret_key = "super secret key"
app.permanent_session_lifetime = timedelta(minutes=5)

myjsonfile = open('./jetson/jetson_config.json','r')
jsondata = myjsonfile.read()
obj = json.loads(jsondata)

userJSON = str(obj['jetson_user'])
passJSON = str(obj['jetson_pass'])


frame_out       = Queue(maxsize=4)


@app.route("/")
def default():
    return redirect("/login")



@app.route("/login", methods=['POST', 'GET'])
def login():
    error = None

    if request.method == 'POST' and request.form['submit_button'] == 'Login':
        user = request.form['user']
        password = request.form['password']
        session['admin'] = userJSON
        session.permanent = True

        if user == userJSON and password == passJSON:
            return redirect('/live', code=302)
        else:
            error = "Username or password not correct"
    elif "admin" in session:
        return redirect(url_for("home"))

    return render_template('/main/index.html', error=error)

@app.route('/logout')
def logout():
    session.pop("admin", None)
    return redirect(url_for('login'))

@app.route("/live")
def home():
    if "admin" not in session:
        return redirect(url_for('login'), code=302)

    return render_template("/main/live.html")

@app.route("/setup/addcam", methods=['POST', 'GET'])
def setup():
    if "admin" not in session:
        return redirect(url_for('login'))

    path = './jetson/'
    filename = 'camera_info'
    data = {}

    if request.method == "POST":
        if request.form['submit_button'] == 'Add':
            data['camera_name'] = request.form['camera_name']
            data['camera_id'] = request.form['camera_id']
            data['camera_link'] = request.form['camera_link']
            jsonToFile(path, filename, data)
            gen(reload=True)
        elif request.form['submit_button'] == 'Check':
            try :
                file = open('jetson/camera_info.json','r')
                fileData = file.read()
                objData = json.loads(fileData)
                camLink = str(objData['camera_link'])

                data['camera_name'] = str(objData['camera_name'])
                data['camera_id'] = str(objData['camera_id'])
                data['camera_link'] = str(objData['camera_link'])               
            except :
                data['camera_name'] = request.form['camera_name']
                data['camera_id'] = request.form['camera_id']
                data['camera_link'] = request.form['camera_link']

            return redirect('/checkcamera?camera_name={}&camera_id={}&camera_link={}'.format(data['camera_name'],data['camera_id'],data['camera_link']), code=302)

    return render_template("/main/setup.html")

@app.route('/setup/zone', methods=['POST', 'GET'])
def zone():
    if "admin" not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.get_json()
        if 'command' not in data:
            location = './jetson/'
            fileName = 'zone_info'
            jsonToFile(location, fileName, data)
            return redirect('/setup/zone?status=success')
            
        else:
            logruncv.info("restart service")
            cmd = 'sudo service jetson restart'
            os.system(cmd)            
        
    return render_template('/main/setup-zone.html')

@app.route('/video_feed', methods=['POST', 'GET'])
def video_feed():
    if "admin" not in session:
        return redirect(url_for('login'))

    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/checkcamera')
def checkcamera():
    if "admin" not in session:
        return redirect(url_for('login'))

    name = request.args.get('camera_name')
    id = request.args.get('camera_id')
    link = request.args.get('camera_link')
    return '''<h2>The Camera Name Is : {}</h2>
              <h2>The Camera Id Is : {}</h2>
              <h2>The Camera Link Is : {}</h2>'''.format(name,id,link)

def jsonToFile(path, filename, data):
    formatFile = './' + path + '/' + filename + '.json'
    with open(formatFile, 'w') as fp:
        json.dump(data, fp)

def gen(reload=False):
    file = open('jetson/camera_info.json','r')
    fileData = file.read()
    objData = json.loads(fileData)
    camLink = str(objData['camera_link'])

    cap = cv2.VideoCapture(camLink)
    logruncv.info(cap)
    logruncv.info("cv2.VideoCapture(camLink) {}".format(camLink))

    if cap.isOpened() == False:
        logruncv.info('Video Not Found')

    while(cap.isOpened()):
        logruncv.info(cap)
        ret, img = cap.read()
        if ret == True:
            # img = cv2.resize(img, (0,0), fx=1.0, fy=1.0)
            img = cv2.resize(img, (1280,720))
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else:
            break
    
    if reload == True:
        cap.release()
        logruncv.info("reload == True")
        return gen()

def logout_asd():
    session.clear()
    return redirect(url_for('login'))


# def core_thread(cam_cfg, modelDetect, detector_lock, interTracker, tracker_lock):
def core_thread(conf, camCfg, detector_lock, frame_out):
    # log information
    logruncv.info('CV get camera ID: {}'.format(camCfg['cam_ID']))
    # logruncv.info('CV counter at line ID: {}'.format(camCfg['lines']))
    rdfCVObj = Core(conf, camCfg, detector_lock, frame_out)
    # process - detect,tracking,counter
    rdfCVObj.process(show_video=True)
    rdfCVObj.close()

    logruncv.info('[INFO] Done process')

def get_config_file (file):
    # with open('config2.json') as f:
    with open(file) as f:
        cam_cfgs = json.load(f)

    return cam_cfgs

        
        
def generate():
    # grab global references to the output frame and lock variables
    global frame_out
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        # with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
        if frame_out.empty():
            time.sleep(0.001)
            # print("empty")
            continue

        # encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", frame_out.get())

        # ensure the frame was successfully encoded
        if not flag:
            # print(flag)
            continue
        time.sleep(0.05)
        # print("success")
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

    

@app.route("/video_feed1")
def video_feed1():
    
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")



def run_core(conf) :
    # bait

    global lock, frame_out

    detector_lock   = threading.Lock()

    logruncv.info('Get camera List to run')
    
    # cam_cfgs = get_config_file()

    # camera_infor = Conf(conf['camera_info'])
    camera_infor    = Conf(conf['camera_info'])
    zone_infor      = Conf(conf['zone_info'])

    if camera_infor['camera_link'] is None or camera_infor['camera_link'] is None or camera_infor['camera_id'] is None :
        raise "camera_infor slack information" 



    if zone_infor['1'] is None or zone_infor['2'] is None or zone_infor['3'] is None :
        raise "zone_infor slack information" 



    cam_cfgs = {}

    cam_cfgs['cam_Link']    = camera_infor['camera_link']
    cam_cfgs['step']        = 1

    cam_cfgs['cam_Name']    = camera_infor['camera_name']
    cam_cfgs['cam_ID']      = camera_infor['camera_id']


    cam_cfgs['funcs'] = []

    zone_fillter = {}
    counter_infor = {}

    zone_fillter["func_ID"]  = 5
    zone_fillter["func_Name"]  = "zone filtter"
    zone_fillter["func_note"]  = decode_note_polygon(zone_infor['1'])


    counter_infor["func_ID"]    = 1
    counter_infor["func_Name"]  = "counter"
    counter_infor["func_line"]  = decode_note_counter(zone_infor['2'])
    counter_infor["func_pont"]  = decode_note_counter(zone_infor['3'])


    cam_cfgs['funcs'].append(zone_fillter)
    cam_cfgs['funcs'].append(counter_infor)

    logruncv.info(cam_cfgs)

    # start 1 thread for 1 camera
    thread = threading.Thread(target=core_thread, args=(conf, cam_cfgs, detector_lock, frame_out))
    thread.daemon = True
    thread.start()
    # start the flask app
    app.run(host='0.0.0.0', port=8888, debug=False,
        threaded=True, use_reloader=False)


if __name__ == '__main__':
    config_server = './jetson/configs.json'
    conf = Conf(config_server)

    run_core(conf)
