from flask import Flask, render_template, flash, request, Response
from imutils.video import VideoStream
from motiondetector import Detective

import threading
import imutils
import datetime
import cv2
import sys
import time

app = Flask(__name__)
app.secret_key = b'xXx_fish_xXx'

lock = threading.Lock()
outframe = None
vid = VideoStream(usePiCamera=1, framerate=2).start()

# @see https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
def detect_motion(framecount):
    global vid, outframe, lock, exit
    det = Detective(0.1)
    total = 0

    while not exit.is_set():
        frame = vid.read()
        frame = imutils.rotate(frame, 180)
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %B %d %Y %I:%M:%S %p"), (85, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (205, 197, 122), 1)

        if total > framecount:
            motion = det.detect(gray)
            if motion:
                fish.moved = True
                fish.is_dead = False
                (thresh, (minx, miny, maxx, maxy)) = motion
                cv2.rectangle(frame, (minx, miny), (maxx, maxy),
                        (205, 197, 122), 2)

        det.update(gray)
        total += 1
        if fish.feeding: # pause video feed when feeding
            time.sleep(7.0)

        with lock:
            outframe = frame.copy()

def generate():
    global outframe, lock, exit
    while not exit.is_set():
        with lock:
            if outframe is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outframe)
            if not flag: continue

        if fish.feeding: # pause video feed when feeding
            time.sleep(7.0)

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')

# the datetime in index.html prevents caching
@app.route("/video_feed")
def video_feed():
    return Response(generate(),
            mimetype="multipart/x-mixed-replace; boundary=frame")

def flash_text():
    if fish.current_period == 0: flash("today is a feeding day")
    if fish.times_fed == 1:
        flash("fish has been fed " + str(fish.times_fed) + " time")
    else:
        flash("fish has been fed " + str(fish.times_fed) + " times")
    if fish.moved: flash("fish has moved today")
    else: flash("fish has not moved today")
    if fish.is_dead: flash("fish is dead")
    else: flash("fish is not dead")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and request.form['request'] == 'feed':
        with lock:
            fish.feed()
    flash_text()
    return render_template('index.html', rand_hash = str(datetime.datetime.now()))

def run_server(in_fish, in_exit):
    global fish, exit
    fish = in_fish
    exit = in_exit

    print('starting server...')
    time.sleep(2.0) # warmup
    task1 = threading.Thread(target=app.run,
            kwargs={'host':'0.0.0.0', 'threaded':True}, 
            daemon=True) 
    task2 = threading.Thread(target=detect_motion, args=(32,), 
            daemon=True) 
    
    task1.start()
    task2.start()
    exit.wait()

    print('shutting down server...')
    sys.exit(0)

