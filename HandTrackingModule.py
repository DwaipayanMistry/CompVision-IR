from unittest import result
import cv2 as cv
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):

        self.mode=mode
        self.maxHands=maxHands
        self.modelComplexity= modelComplexity
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        # pass
        self.mpHands= mp.solutions.hands
        self.hands= self.mpHands.Hands(self.mode, self.maxHands,modelComplexity,
                                        self.detectionCon,
                                        self.trackCon)
        self.mpDraw= mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB= cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results= self.hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                    self.mpHands.HAND_CONNECTIONS)
    
        return img


    def findHandPosition(self, img, handNo=0, draw=True):
        landmarkList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                ix, iy = int(lm.x * w), int(lm.y * h)
                landmarkList.append([id, ix, iy])

                if draw:
                    cv.circle(img, (ix, iy), 10, (255, 255, 255), cv.FILLED)

        return landmarkList



def main():
    landmarkList=[]
    pTime= 0
    cTime= 0
    captureV= cv.VideoCapture(0)
    det= handDetector()
    while True:
        success, img= captureV.read()
        img= det.findHands(img)
        landmarkList= det.findHandPosition(img)
        
        if len(landmarkList)!= 0:
            print(landmarkList[0])
        
        cTime= time.time()
        fps= 1/(cTime-pTime)
        pTime= cTime
        cv.putText(img,str(int(fps))+'fps', (10,35), cv.FONT_HERSHEY_COMPLEX_SMALL,2,(225,200,0),2)
        
        cv.imshow('Image', img)
        if cv.waitKey(20) & 0xFF==ord('c'):
            break

if __name__== "__main__":
    main()