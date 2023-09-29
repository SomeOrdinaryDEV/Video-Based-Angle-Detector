import numpy as np
from skimage.transform import (hough_line, hough_line_peaks)
import cv2
from matplotlib import pyplot as plt
import time

cap = cv2.VideoCapture('Video Data/Vid1.mov')
counter = 1
frame_second = 0
angle_addition = 0 
cur_angle = 0
anglelist = []
mean = 0

def angles(edges):
    tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 180)
    hspace, theta, dist = hough_line(edges, tested_angles)
    h, q, d = hough_line_peaks(hspace, theta, dist)
    angle_list = []
        
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    ax = axes.ravel()

    
    origin = np.array((0, edges.shape[1]))

    for _, angle, dist in zip(*hough_line_peaks(hspace, theta, dist)):
        angle_list.append(angle) #Not for plotting but later calculation of angles
        y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)

    angles = [a*180/np.pi for a in angle_list]

    # Compute difference between the two lines
    angle_difference = np.max(angles) - np.min(angles)
    return angle_difference

#use cartesian reference frame
#point clusters(hough lines, hough peaks) 

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Our operations on the frame come here
    edges = cv2.Canny(cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), (11,11), 0), 100, 170)    
    
    if counter % 3 == 0:
        angle_difference = angles(edges)
        angle_addition = angle_addition + angle_difference
        if counter%30 == 0:
            anglelist.append((round(angle_addition/10, 2)))
            print(anglelist[frame_second])
            angle_addition = 0
            frame_second = frame_second + 1
        
         
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    plt.close('all')
    counter = counter + 1
anglelist.sort()
print('end of angles, start of list')

for i in range(len(anglelist)):
    print(anglelist[i])
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()