# Laft hand detector

import cv2 as cv
import time
import os
import HandTrackingModule as htm
#Reading videos

width= 640
height= 480
cap = cv.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
pTime=0
tipIds=[4, 8, 12, 16, 20]

det= htm.handDetector(detectionCon=00.68)
while True:
    isTrue, frame = cap.read()
    frame=det.findHands(frame)
    landmarkList=det.findHandPosition(frame, draw= False)
    # print(landmarkList)
    
    if len(landmarkList)!= 0:
        fingers=[]
        if landmarkList[tipIds[0]][1] < landmarkList[tipIds[0]-1][1]:
        # print("pinky finger Open")
            fingers.append(1)    
        else:
            fingers.append(0)

        for id in range(1,5):
            if landmarkList[tipIds[id]][2]< landmarkList[tipIds[id]-2][2]:
                # print("pinky finger Open")
                fingers.append(1)    
            else:
                fingers.append(0)
        totalFinger= fingers.count(1)
        # print(totalFinger)
        cv.putText(frame, str(totalFinger)+ 'Fingers are open', (25,80), cv.FONT_HERSHEY_COMPLEX_SMALL,2,(225,00,0),1)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(frame, str(int(fps))+'fps', (10,35), cv.FONT_HERSHEY_COMPLEX_SMALL,2,(225,200,0),2)
    
    cv.imshow('Video', frame)
    if cv.waitKey(20) & 0xFF==ord('c'):
        break