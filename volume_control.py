import cv2
import numpy as np
import time 
import mediapipe as mp
import handtracking_module as htm

ptime=0
cap=cv2.VideoCapture(0) # Open the camera
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
cap.set(3,640) # Set the width of the camera    
cap.set(4,480) # Set the height of the camera
detector=htm.handDetector(detectionCon=0.7) # Create an instance of the hand detector class


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
volBar=400
minVol=volRange[0] # Get the minimum volume level
maxVol=volRange[1] # Get the maximum volume level
while True:
    success,img=cap.read() 
    img=detector.findHands(img) 
    lmlist=detector.findPosition(img,draw=False) 
    if len(lmlist)!=0:
        # print(lmlist)
        # print(lmlist[4],lmlist[8]) # Print the coordinates of the thumb and index finger
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED) # Draw a circle on the thumb
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED) # Draw a circle on the index finger
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)

        length=np.hypot(x2-x1,y2-y1) # Calculate the distance between the thumb and index finger
        # print(length)
        if length<40:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
        #length range 40-220
        # vol range -65 to 0
        vol = np.interp(length, [40, 220], [minVol, maxVol])
        volBar=np.interp(length,[40,220],[400,150]) # Map the length to the volume bar height
        print(volBar)
        # print(vol,length)
        volume.SetMasterVolumeLevel(vol, None)
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0,255, 0), cv2.FILLED)
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f'FPS:{int(fps)}',(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3) # Display the FPS on the image
    cv2.imshow("Image",img)
    cv2.waitKey(1) # Wait for 1 ms before displaying the next frame
