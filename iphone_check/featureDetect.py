import numpy as np
import cv2
from matplotlib import pyplot as plt
import scipy as sp

img = cv2.imread("newpic.png")
img1 = cv2.imread("newpic.png", 0)

#start = cv2.FeatureDetector_create("STAR")
start = cv2.FeatureDetector_create("GFTT")
start.setDouble("qualityLevel", 0.01)
start.setDouble("minDistance", 1.)
start.setBool("useHarrisDetector", False)
start.setDouble("k", 0.4)
#brief = cv2.DescriptorExtractor_create("BRIEF")

kp = start.detect(img1, None)
kp, des = start.compute(img1, kp)

img2 = cv2.drawKeypoints(img, kp, color=(0,255,0), flags=0)
cv2.imshow("winname", img2)
cv2.waitKey(0)