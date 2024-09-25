import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
import requests

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("./Model/keras_model.h5", "./Model/labels.txt")
offset = 20
imgSize = 300
counter = 0

labels = ["Hello", "I love you", "No", "Okay", "Please", "Thank you", "Yes"]
interval_duration = 5  # Interval duration in seconds
start_time = time.time()  # Start time for interval
timer_font = cv2.FONT_HERSHEY_SIMPLEX

outputs = []  # List to store outputs during an interval

# Initial 10 seconds delay
while time.time() - start_time < 10:
    _, _ = cap.read()

start_time = time.time()  # Reset start time after the initial delay

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap: wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap: hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        cv2.rectangle(imgOutput, (x - offset, y - offset - 70), (x - offset + 400, y - offset + 60 - 50), (0, 255, 0),
            cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (0, 255, 0), 4)

        if counter > 10 and counter % interval_duration == 0:
            if labels[index] not in outputs:
                outputs.append(labels[index])  # Store output during this iteration

                # Send output to Flask server
                requests.post('http://localhost:5000/store_output', json={'output': labels[index]})

    current_time = time.time() - start_time

    # Display timer
    cv2.putText(imgOutput, "Time: {:.2f}".format(current_time), (50, 50), timer_font, 1, (255, 0, 0), 2)

    cv2.imshow('Image', imgOutput)
    key = cv2.waitKey(1)

    # Check if the window is closed
    if key == ord('q') or cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:
        break  # Exit the loop

    counter += 1

# Print outputs when the window is closed
print("Outputs when the window is closed:")
print(*outputs)

# Release resources
cap.release()
cv2.destroyAllWindows()
