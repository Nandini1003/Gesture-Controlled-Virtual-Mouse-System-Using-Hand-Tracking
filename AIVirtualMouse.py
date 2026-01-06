import cv2
import numpy as np
import mediapipe as mp
import time
import math
import autopy
import pyautogui
import screen_brightness_control as sbc

pyautogui.FAILSAFE = False

# ---------------- CONFIG ----------------
wCam, hCam = 640, 480
frameR = 100
dead_zone = 4
min_smooth = 3
max_smooth = 10
scroll_sensitivity = 3
zoom_sensitivity = 5

# ---------------- HAND DETECTOR ----------------
class handDetector:
    def __init__(self, detectionCon=0.5, trackCon=0.5):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img):
        lmList = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            h, w, _ = img.shape
            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)
        return lmList

    def fingersUp(self, lmList):
        fingers = [0, 0, 0, 0, 0]
        if not lmList:
            return fingers

        # Thumb
        fingers[0] = lmList[4][1] > lmList[3][1]

        # Other fingers
        for i in range(1, 5):
            fingers[i] = lmList[self.tipIds[i]][2] < lmList[self.tipIds[i]-2][2]
        return fingers

    def findDistance(self, p1, p2, lmList):
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        return math.hypot(x2 - x1, y2 - y1)


# ---------------- MAIN ----------------
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = handDetector()
wScr, hScr = autopy.screen.size()

plocX, plocY = 0, 0
prev_scroll_y = None
prev_brightness_x = None
drag_active = False
prev_click = False
pTime = 0

while True:
    success, img = cap.read()
    if not success:
        continue

    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    fingers = detector.fingersUp(lmList)

    if lmList:
        x_index, y_index = lmList[8][1:]
        x_middle, y_middle = lmList[12][1:]
        x_thumb, y_thumb = lmList[4][1:]

        # ---------------- MOVE CURSOR ----------------
        if fingers == [0, 1, 0, 0, 0]:
            x3 = np.interp(x_index, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y_index, (frameR, hCam - frameR), (0, hScr))

            dx, dy = x3 - plocX, y3 - plocY
            dist = np.hypot(dx, dy)
            smooth = int(np.clip(dist / 10, min_smooth, max_smooth))
            clocX = plocX + dx / smooth
            clocY = plocY + dy / smooth

            autopy.mouse.move(wScr - clocX, clocY)
            plocX, plocY = clocX, clocY

        # ---------------- SCROLL ----------------
        if fingers == [0, 1, 0, 0, 0]:
            if prev_scroll_y:
                pyautogui.scroll(int((prev_scroll_y - y_index) * scroll_sensitivity))
            prev_scroll_y = y_index
        else:
            prev_scroll_y = None

        # ---------------- LEFT CLICK ----------------
        if fingers == [0, 0, 1, 0, 0] and not prev_click:
            autopy.mouse.click()
            prev_click = True
            time.sleep(0.2)
        if fingers != [0, 0, 1, 0, 0]:
            prev_click = False

        # ---------------- RIGHT CLICK ----------------
        if fingers == [0, 1, 1, 1, 0]:
            autopy.mouse.click(autopy.mouse.Button.RIGHT)
            time.sleep(0.3)

        # ---------------- DRAG & DROP ----------------
        if sum(fingers) == 0:
            if not drag_active:
                pyautogui.mouseDown()
                drag_active = True
        else:
            if drag_active:
                pyautogui.mouseUp()
                drag_active = False

        # ---------------- ZOOM ----------------
        if fingers[0] == 1 and fingers[1] == 1 and sum(fingers) == 2:
            dist = detector.findDistance(4, 8, lmList)
            zoom = int((200 - dist) / zoom_sensitivity)
            if zoom != 0:
                pyautogui.keyDown('ctrl')
                pyautogui.scroll(zoom)
                pyautogui.keyUp('ctrl')

        # ---------------- BRIGHTNESS ----------------
        if fingers == [1, 1, 1, 1, 1]:
            dist = detector.findDistance(4, 8, lmList)
            if dist < 40:
                if prev_brightness_x:
                    dx = x_index - prev_brightness_x
                    try:
                        curr = sbc.get_brightness()[0]
                        sbc.set_brightness(np.clip(curr + int(dx / 5), 0, 100))
                    except:
                        pass
                prev_brightness_x = x_index
        else:
            prev_brightness_x = None

    # ---------------- FPS ----------------
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 40),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("AI Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
