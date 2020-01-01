from road_recognition import RoadRecognition
import cv2

while True:

    img = cv2.imread('./test_image/black.jpg')
    RR = RoadRecognition()
    RR.recognize(img)
