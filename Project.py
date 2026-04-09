import cv2
import mediapipe as mp
import serial
import time

# 🔥 Change this port for Mac
arduino = serial.Serial(port='/dev/cu.usbmodem14101', baudrate=9600, timeout=1)
time.sleep(2)

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Finger detection function
def detect_fingers(image, hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    finger_states = [0, 0, 0, 0, 0]

    # Thumb
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        finger_states[0] = 1

    # Other fingers
    for idx, tip in enumerate(finger_tips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[idx + 1] = 1

    return finger_states

# Start camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers_state = detect_fingers(image, hand_landmarks)

            # Send data to Arduino
            arduino.write(bytes(fingers_state))
            print("Fingers:", fingers_state)

    cv2.imshow('Hand Tracking', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()