
# importing the module
import cv2
import numpy as np
import alignhelper as im
# import stagecontrol as mdt
import matplotlib.pyplot as plt
import waveguidehelper

#initialize images, set bw and straight to empty
img_source = cv2.imread('3straightened.png')

#Mouse callback commands
def straight_img_click(event, x, y, flags, param):

    #left click, show percentiles and plot
    if event == cv2.EVENT_LBUTTONDOWN:
        row = img_source[y]

        #plot
        plt.figure()
        ys = row
        markers_on = np.array([x])
        plt.plot(ys, '-g.',  mfc='red', mec='k', markevery=markers_on)
        #minimum
        plt.hlines((np.percentile(row, 0)), 0, len(row))
        #maximum
        plt.hlines((np.percentile(row, 100)), 0, len(row))
        #median
        plt.hlines((np.percentile(row, 50)), 0, len(row))
        #10th percentile
        plt.hlines((np.percentile(row, 10)), 0, len(row))

        plt.show(block = False)
    
    if event == cv2.EVENT_RBUTTONDOWN:
        row = img_source[y]

        plt.figure()
        (low, high) = waveguidehelper.narrow_down(row, x, 10, 50)
        local_maxima = waveguidehelper.local_max(row[low:high])[0]
        #markers_on = np.array([x-low])
        markers_on = local_maxima
        plt.plot(row[low:high], '-g.', mfc='red', mec='k', markevery=markers_on)
        print(x-low)
        plt.show(block = False)





#Open windows
cv2.namedWindow("Straight Image")

#Detect clicks
cv2.setMouseCallback("Straight Image", straight_img_click)

while True:
    cv2.imshow("Straight Image", img_source)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()

#move on to shifting procedure


cv2.namedWindow("hello") 
cv2.waitKey(0)
cv2.destroyAllWindows()