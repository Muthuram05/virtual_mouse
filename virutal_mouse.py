import cv2
import numpy as np
import hand_tracking_module as htm
import time
import autopy

wcam, hcam = 640, 480
ptime = 0
detector = htm.handDetector(maxHands=1)
wscr, hscr = autopy.screen.size()
framer = 100
smooth=5
plocx,plocy=0,0
clocx,cloy=0,0

capture = cv2.VideoCapture(0)
capture.set(3, wcam)
capture.set(4, hcam)
while True:
    _, img = capture.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #print(x1,y1,x2,y2)

        fingers = detector.fingersup()
        #print(fingers)
        if fingers[1] and fingers[2] == 0:
            cv2.rectangle(img,(framer,framer), (wcam-framer, hcam-framer), (255,255,0),2)
            x3 = np.interp(x1,(framer,wcam-framer),(0,wscr))
            y3 = np.interp(y1, (framer, hcam-framer), (0, hscr))
            clocx=plocx+(x3-plocx)/smooth
            clocy = plocy + (y3 - plocy) / smooth

            autopy.mouse.move(wscr-clocx,clocy)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            plocx,plocy = clocx,clocy
        if fingers[1] == 1 and fingers[2] == 1:
            length,img,info=detector.findDistance(8, 12, img)
            print(length)
            if length < 40:
                cv2.circle(img, (info[4], info[5]), 15, (0, 255, 0, cv2.FILLED))
                autopy.mouse.click()





    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (20, 50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("image", img)
    key=cv2.waitKey(1)
    if key == 27:
        quit()