import cv2
import mediapipe as mp
import time
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
                        static_image_mode=self.mode,
                        max_num_hands=self.maxHands,
                        min_detection_confidence=self.detectionCon,
                        min_tracking_confidence=self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils
    
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
        return img
    
    
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:  # Check if hands are detected ,this function return a list of hands detected
            myHand = self.results.multi_hand_landmarks[handNo] # Get the specified hand 
            for id, lm in enumerate(myHand.landmark): 
                # print(id, lm)
                h, w, c = img.shape 
                cx, cy = int(lm.x * w), int(lm.y * h) # Get the coordinates of the landmark in pixels
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    if lmList[id][0]==4:
                        cv2.circle(img, (cx, cy), 15, (0, 255, 255), cv2.FILLED)
        return lmList # Return the list of landmarks with their ids and coordinates
