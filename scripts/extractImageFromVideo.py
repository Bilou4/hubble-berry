#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
cap = cv2.VideoCapture('/path/to/video')
count = 0
while cap.isOpened():
    ret,frame = cap.read()
    cv2.imshow('window-name',frame)
    cv2.imwrite("/path/to/output/frame%d.jpg" % count, frame)
    count = count + 1
    if cv2.waitKey(10) & 0xFF == ord('q'): # press q to exit the program
        break


cap.release()
cv2.destroyAllWindows()  # destroy all the opened windows

