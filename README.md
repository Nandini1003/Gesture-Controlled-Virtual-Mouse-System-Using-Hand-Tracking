# Gesture Controlled Virtual Mouse System Using Hand Tracking
Control your mouse, scrolling, zoom, drag-and-drop, and system interactions using hand gestures captured through a webcam — no physical mouse required.

This project uses MediaPipe + OpenCV for real-time hand tracking and maps distinct finger gestures to mouse and system actions.

Features

i. Cursor movement using index finger

ii. Left click, right click via finger gestures

iii. Smooth scrolling using single finger

iv. Drag & Drop using fist gesture

v. Zoom in / Zoom out using pinch gesture

Gesture Mapping

| Gesture     | Fingers Used                    | Action         |
| ----------- | ------------------------------- | -------------- |
| Cursor Move | Index finger up                 | Move mouse     |
| Scroll      | Index finger up (vertical move) | Scroll up/down |
| Left Click  | Middle finger up                | Left click     |
| Right Click | Index + Middle + Ring up        | Right click    |
| Drag & Drop | All fingers down (fist)         | Drag / Release |
| Zoom In     | Thumb + Index pinch inward      | Zoom in        |
| Zoom Out    | Thumb + Index pinch outward     | Zoom out       |

Tech Stack

Language: Python 3.10+
Computer Vision: OpenCV
Hand Tracking: MediaPipe
Mouse Control: AutoPy
Gesture Handling: NumPy
System Interaction: PyAutoGUI

Installation (With Versions)

 Use Python 3.10 or 3.11 for best compatibility

1. Create Virtual Environment (Recommended)
  ``` # python -m venv venv # ```
2. Install Required Libraries
   ``` 
         pip install opencv-python==4.9.0.80
         pip install mediapipe==0.10.9
         pip install numpy==1.26.4
         pip install autopy==4.0.0
         pip install pyautogui==0.9.54
   ```
3. How to Run
   ``` python virtual_mouse.py ```

Project Structure
```
AI-Virtual-Mouse/
│
├── HandTrackingModule.py
├── virtual_mouse.py
├── README.md
├── requirements.txt
└── assets/
```

Libraries to install
```
opencv-python==4.9.0.80
mediapipe==0.10.9
numpy==1.26.4
autopy==4.0.0
pyautogui==0.9.54
```








