import cv2
import sys
sys.path.append('/home/pi/autopilot/')
from road_recognition import RoadRecognition

RR = RoadRecognition()
img = cv2.imread('test_image/test23.jpg') #9 18 19 22 23
RR.testOneImage(img)
