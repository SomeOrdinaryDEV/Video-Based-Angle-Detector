import numpy as np
from skimage.transform import (hough_line, hough_line_peaks)
import cv2
from matplotlib import pyplot as plt
# reflection problems on computer vision
# distortion problems (non visible solid edges)
# use opencv vision tracker 


cap = cv2.VideoCapture('Video Data/Vid1.mov')
counter = 1
angle_addition = 0 
str_angle = ""
#use cartesian reference frame
#point clusters(hough lines, hough peaks) 

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret == False:
       cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
       continue
    # Our operations on the frame come here
    edges = cv2.Canny(cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), (11,11), 0), 100, 170)
    #gray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
    lines = cv2.HoughLinesP(edges, 35, np.pi/180, 50, maxLineGap=10)
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
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
    if counter % 30 != 0:
        angle_addition = angle_addition + angle
    else:
        angle_addition = angle_addition/30
    
    if round(180 - angle_difference, 3) >= round(angle_difference, 3) and angle_difference >= 90:
        print(round(180 - angle_difference, 3))  #Subtracting from 180 to show it as the small angle between two lines
        str_angle = str (round(180- angle_difference), 3)
        cv2.putText(frame, str_angle, (150,200), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
    else:
        print(round(angle_difference, 3))
        str_angle = str (round(angle_difference, 3))
        cv2.putText(frame, str_angle, (150,200), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
    plt.close('all')
        

    counter = counter + 1
    cv2.imshow('edges after hough lines', edges)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("frame", frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
