import cv2 # import libraries
import numpy as np
import time

cap = cv2.VideoCapture(0)# takes videofeed from input 0
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000) #dimensions of videofeed window
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)



prev = [0, 0] #to store x, y coordinates for
maxareaold=0 # global variables
countc=0# counters for closer, farther
countf=0
while (1):

    start_time = time.time()
    ret, frame = cap.read()
    blur = cv2.blur(frame, (3, 3)) # edge smoothening (image smoothening) - to make it easier to identify hand outlines

    # Convert to HSV color space
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) # hue saturation value

    # Skin Color Detection: hsv values between array 1 and 2 are for skin color
    mask2 = cv2.inRange(hsv, np.array([2, 50, 50]), np.array([15, 255, 255]))

    # initialised arrays for erosion and dilation (convolution)
    # Reference (Which shape of kernel) - https://stackoverflow.com/questions/49201570/choosing-right-structuring-element
    kernel_square = np.ones((11, 11), np.uint8) # white square for erosion - to reduce noise
    # to preserve curves in image
    kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) # white ellipse for dilation - to reduce extra erosion

    # Filtering
    # Reference: https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
    dilation = cv2.dilate(mask2, kernel_ellipse, iterations=1)
    erosion = cv2.erode(dilation, kernel_square, iterations=1)
    dilation2 = cv2.dilate(erosion, kernel_ellipse, iterations=1)
    filtered = cv2.medianBlur(dilation2, 5) # median blur for image smoothening
    kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    dilation2 = cv2.dilate(filtered, kernel_ellipse, iterations=1)
    kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilation3 = cv2.dilate(filtered, kernel_ellipse, iterations=1)
    median = cv2.medianBlur(dilation2, 5)
    ret, thresh = cv2.threshold(median, 127, 255, 0) # convert to black and white
    cv2.imshow('threshold', thresh) # prints black and white screen
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # finds contours to identify hand boundaries
    #cv2.drawContours(frame, contours, -1, (122,122,0), 3)
    max_area = 100
    ci = 0 # index of contours - list of points for each separate white object
    #Assuming largest area of skin color is hand
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if (area > max_area):
            max_area = area
            ci = i
    print('index : ' + str(ci))
    if ci != 0:
        cnts = contours[ci]
    else:
        cv2.putText(frame, 'Hand Not Found', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)

    hull = cv2.convexHull(cnts) # creates white boundary in frame connecting all points for largest skin color area 

    moments = cv2.moments(cnts) # to find centre of mass or area of object


    if moments['m00'] != 0: # calculate centre of mass according to https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
    centerMass = (cx, cy)

    # print("x : " + str(cx))
    # print("y : " + str(cy))
    #
    # Logic for Closer/Farther - Based on change in max_area
    if(max_area>maxareaold and countc==5):
        cv2.putText(frame, 'Closer',(550,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2)
        print("Closer")
        countc=0
        countf=0
    elif(max_area>maxareaold):
        countc=countc+1
        countf=0
    elif(max_area<maxareaold and countf==5):
        cv2.putText(frame, 'Farther',(550,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2)
        print("Farther")
        countc=0
        countf=0
    elif(max_area<maxareaold):
        countf=countf+1
        countc=0
    
    maxareaold=max_area   

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Logic for Left, Right, Up, Down

    if (cx - prev[0] > 0 and abs(cx - prev[0]) > 10):
        # print('abs diffX : ' + str(abs(cx - prev[0])))
        cv2.putText(frame, 'Left', (50, 200), font, 2, (255, 255, 255), 2)
        print('Left')
    elif (cx - prev[0] < 0 and abs(cx - prev[0]) > 10):
        # print('diffX' + str(x - prev[0]))
        # print('abs diffX : ' + str(abs(cx - prev[0])))
        cv2.putText(frame, 'Right', (50, 300), font, 2, (255, 255, 255), 2)
        print('Right')
    elif (cy - prev[1] > 0 and abs(cy - prev[1]) > 10):
        # print('diffY' + str(cy - prev[1]))
        # print('abs diffY : ' + str(abs(cy - prev[1])))
        print('Up')
        cv2.putText(frame, 'Down', (50, 400), font, 2, (255, 255, 255), 2)
    elif (cy - prev[1] < 0 and abs(cy - prev[1]) > 10):
        # print('diffY' + str(cy - prev[1]))
        # print('abs diffY : ' + str(abs(cy - prev[1])))
        print('Down')
        cv2.putText(frame, 'Up', (50, 500), font, 2, (255, 255, 255), 2)
    prev[0] = cx
    prev[1] = cy

    cv2.circle(frame, centerMass, 7, [100, 0, 255], 2) # to display center mass in window
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'Center', tuple(centerMass), font, 2, (255, 255, 255), 2) #put text at Center Mass
    #draw bounding rectangle for hand
    x, y, w, h = cv2.boundingRect(cnts)
    img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.drawContours(frame, [hull], -1, (255, 255, 255), 2)
    cv2.imshow('Image', frame)
    k = cv2.waitKey(5) & 0xFF # Close window on esc key
    if k == 27: #27 is esc key code
        break

cap.release()
cv2.destroyAllWindows()