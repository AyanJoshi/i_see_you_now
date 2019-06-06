import time
import socket
import threading
import signal
import sys
import pygst
import cv2
import numpy as np
if __name__ == "__main__":
 
    #NEW STUFF
    cap = cv2.VideoCapture('Recording005.mp4')
    #cap = cv2.VideoCapture('rtsp://TG02B-080105021271:TobiiGlasses@10.218.105.198:80/1')
    #cap = cv2.VideoCapture('rtsp://10.218.105.198:80/1')
    #cap.open('rtsp://TG02B-080105021271:TobiiGlasses@10.218.105.198:80/1');
    #cap.open('rtsp://10.218.105.198:80')
    #while cap.isOpened() == False:
	#cap = cv2.VideoCapture('rtsp://TG02B-080105021271:TobiiGlasses@10.218.105.198:80/1')
	#cap.open('rtsp://TG02B-080105021271:TobiiGlasses@10.218.105.198:80');
	#print('cap is closed')
    #print('cap opened')
    #k = cap.isOpened()
    #if k == False:
	#print('cap was closed')
	#cap.open('rtsp://TG02B-080105021271:TobiiGlasses@10.218.105.198:80');
    #k = cap.isOpened()
    #if k == False:
	#print('cap is still closed') 
    cap.set(3, 640) #WIDTH
    cap.set(4, 480) #HEIGHT
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #NEW STUFF /END

    while True:
	print('YOOO')
        # Read live data
	#NEW STUFF
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
        #NEW STUFF /END
    cap.release()
    cv2.destroyAllWindows()
