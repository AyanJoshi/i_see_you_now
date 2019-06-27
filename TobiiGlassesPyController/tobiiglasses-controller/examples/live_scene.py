# live_scene.py : A demo for video streaming
#
# Copyright (C) 2019  Davide De Tommaso
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>
import time
import socket
import threading
import signal
import sys
import pygst
import cv2
import numpy as np
from tobiiglassesctrl.controller import TobiiGlassesController
address = "10.218.107.188"
#address = "fe80::76fe:48ff:ff00:ff00"
cap = cv2.VideoCapture("rtsp://%s:8554/live/scene" % address)
tobiiglasses = TobiiGlassesController("10.218.107.188")
tobiiglasses.start_streaming()
# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")
#NEW STUFF
# cap.set(3, 640) #WIDTH
# cap.set(4, 480) #HEIGHT
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#/NEW STUFF

#NEW STUFF 2
# tobiiglasses = TobiiGlassesController("10.218.107.188")
# print(tobiiglasses.get_battery_status())

# tobiiglasses.start_streaming()
#/NEW STUFF 2

# Read until video is completed
while(1):
  # Capture frame-by-frame
  ret, frame = cap.read()
  #NEW STUFF
  # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  #/NEW STUFF
  if ret == True:
    # print(len(faces))
    # for (x,y,w,h) in faces:
    #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    #     roi_gray = gray[y:y+h, x:x+w]
    #     roi_color = frame[y:y+h, x:x+w]

    # Display the resulting frame
    cv2.imshow('Tobii Pro Glasses 2 - Live Scene',frame)
    # print("Left Eye: %s " % tobiiglasses.get_data()['left_eye'])
    # print("Right Eye: %s " % tobiiglasses.get_data()['right_eye'])
    print("Gaze Position: %s " % tobiiglasses.get_data()['gp'])
    # Press Q on keyboard to  exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break
tobiiglasses.stop_streaming()
tobiiglasses.close()
# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
