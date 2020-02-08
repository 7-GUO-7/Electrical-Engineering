import cv2
import sys, os, time
dataset='Dataset'
img1 = cv2.imread('target.jpg', cv2.IMREAD_COLOR)


sift =cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
min=100
answer='none'
t0=time.clock()
for root, dirs, files in os.walk(dataset):
    for filename in files:
        img2 = cv2.imread(os.path.join(root, filename),cv2.IMREAD_COLOR)
        kp2, des2 = sift.detectAndCompute(img2, None)
        bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
        matches = bf.match(des1, des2)
        re = matches[0].distance
        if re<min:
            min=re
            answer=filename
t1=time.clock()
print 'NN:'
print 'distance:',min
print 'best picture:',answer
print t1-t0






orb = cv2.ORB_create()
t0=time.clock()
kp1, des1 = orb.detectAndCompute(img1, None)
min=100
answer='none'
for root, dirs, files in os.walk(dataset):
    for filename in files:
        img2 = cv2.imread(os.path.join(root, filename),cv2.IMREAD_COLOR)
        kp2, des2 = orb.detectAndCompute(img2, None)
    # print(kp1)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        re = matches[0].distance
        if re<min:
            min=re
            answer=filename
t1=time.clock()
print 'LSH:'
print 'distance:',min
print 'best picture:',answer
print t1-t0