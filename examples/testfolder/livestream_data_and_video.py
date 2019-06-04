'''
    Example for how to receive live data and display live video (without gaze overlay) from glasses.
    gstreamer 0.10 required in order to display live video.

    Note: This example program is *only* tested with Python 2.7 on Ubuntu 12.04 LTS
          and Ubuntu 14.04 LTS (running natively).
'''
import time
import socket
import threading
import signal
import sys
import pygst
import cv2
import numpy as np

pygst.require('0.10')
import gst

timeout = 1.0
running = True


GLASSES_IP = "fe80::76fe:48ff:fe2b:151e%eth0" # IPv6 address scope global
#GLASSES_IP = "10.218.104.64"  # IPv4 address
PORT = 49152

# Keep-alive message content used to request live data and live video streams
KA_DATA_MSG = "{\"type\": \"live.data.unicast\", \"key\": \"some_GUID\", \"op\": \"start\"}"
KA_VIDEO_MSG = "{\"type\": \"live.video.unicast\", \"key\": \"some_other_GUID\", \"op\": \"start\"}"


# Gstreamer pipeline definition used to decode and display the live video stream
PIPELINE_DEF = "udpsrc do-timestamp=true name=src blocksize=1316 closefd=false buffer-size=5600 !" \
               "mpegtsdemux !" \
               "queue !" \
               "ffdec_h264 max-threads=0 !" \
               "ffmpegcolorspace !" \
               "xvimagesink name=video"


# Create UDP socket
def mksock(peer):
    iptype = socket.AF_INET
    if ':' in peer[0]:
        iptype = socket.AF_INET6
    return socket.socket(iptype, socket.SOCK_DGRAM)


# Callback function
def send_keepalive_msg(socket, msg, peer):
    while running:
        print("Sending " + msg + " to target " + peer[0] + " socket no: " + str(socket.fileno()) + "\n")
        socket.sendto(msg, peer)
        time.sleep(timeout)


def signal_handler(signal, frame):
    stop_sending_msg()
    sys.exit(0)


def stop_sending_msg():
    global running
    running = False


if __name__ == "__main__":
    #NEW STUFF
    cap = cv2.VideoCapture(-1)
    #cap = cv2.VideoCapture('rtsp://TG02B-080105021271:TobiiGlasses@fe80::76fe:48ff:fe2b:151e%eth0:49152/1')
    #cap = cv2.VideoCapture('rtsp://fe80::76fe:48ff:fe2b:151e%eth0:49152/1')
    #cap.open('rtsp://TG02B-080105021271:TobiiGlasses@10.218.105.198:80');
    #cap.open('rtsp://fe80::76fe:48ff:fe2b:151e:49152')
    k = cap.isOpened()
    if k == False:
	print('cap was closed')
	#cap.open('rtsp://TG02B-080105021271:TobiiGlasses@10.218.105.198:80');
    #k = cap.isOpened()
    #if k == False:
	#print('cap is still closed') 
    cap.set(3, 640) #WIDTH
    cap.set(4, 480) #HEIGHT
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #NEW STUFF /END

    signal.signal(signal.SIGINT, signal_handler)
    peer = (GLASSES_IP, PORT)

    # Create socket which will send a keep alive message for the live data stream
    data_socket = mksock(peer)
    td = threading.Timer(0, send_keepalive_msg, [data_socket, KA_DATA_MSG, peer])
    td.start()

    # Create socket which will send a keep alive message for the live video stream
    video_socket = mksock(peer)
    tv = threading.Timer(0, send_keepalive_msg, [video_socket, KA_VIDEO_MSG, peer])
    tv.start()

    # Create gstreamer pipeline and connect live video socket to it
    pipeline = None
    try:
        pipeline = gst.parse_launch(PIPELINE_DEF)
    except Exception, e:
        print e
        stop_sending_msg()
        sys.exit(0)

    src = pipeline.get_by_name("src")
    src.set_property("sockfd", video_socket.fileno())

    pipeline.set_state(gst.STATE_PLAYING)
 
    while running:
	print('YOOO')
        # Read live data
        data, address = data_socket.recvfrom(1024)
	print (data)
	#NEW STUFF
        #if cap.isOpened() == True:
	print('cap is open')
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	print(len(faces))
	for (x,y,w,h) in faces:
        	cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        	roi_gray = gray[y:y+h, x:x+w]
        	roi_color = frame[y:y+h, x:x+w]
	cv2.imshow('frame',frame)
    	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break
	#elif cap.isOpened() == False:
	#	print('cap is not opened')
	#	cap.open('rtsp://TG02B-080105021271:TobiiGlasses@10.218.105.198:80/1')
        #NEW STUFF /END
	state_change_return, state, pending_state = pipeline.get_state(0)

        if gst.STATE_CHANGE_FAILURE == state_change_return:
            stop_sending_msg()
    cap.release()
    cv2.destroyAllWindows()
