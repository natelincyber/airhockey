import cv2
import numpy as np

#51, 106, 0, 111, 202, 234
kernel = np.ones((5,5),np.uint8)


def nothing(x):
    pass


def thresholding(h, s, v, hM, sM, vM):

    cap = cv2.VideoCapture(1)
    
    # Initialize HSV min/max values

    hMin = h
    sMin = s
    vMin = v

    hMax = hM
    sMax = sM
    vMax = vM


    while(1):

        ret, image = cap.read()

        # Set minimum and maximum HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Convert to HSV format and color threshold
        filter = cv2.bilateralFilter(image, 10, 80, 80)
        hsv = cv2.cvtColor(filter, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        
        
        ret, th1 = cv2.threshold(
            mask, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        th2 = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)


        ret, th2 = cv2.threshold(
            th2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(th2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            # TODO mess with area given the distance from the table to the puck
            if area > 3000:
                cv2.drawContours(image, contour, -1, (0,255,0))
                rect = cv2.boundingRect(contour)
                x,y,w,h = rect
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.putText(image,f'Object @ ({x+w/2},{y+h/2})',(x,y+h+10),0,0.3,(0,255,0))
        
        # Display result image
        cv2.imshow('image', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return


def tuneHSV(h, s, v, hM, sM, vM):


    cap = cv2.VideoCapture(1)
    cv2.namedWindow('HSV Values', cv2.WINDOW_NORMAL)

    # Create trackbars for color change
    # Hue is from 0-179 for Opencv
    cv2.createTrackbar('HMin', 'HSV Values', 0, 179, nothing)
    cv2.createTrackbar('SMin', 'HSV Values', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'HSV Values', 0, 255, nothing)
    cv2.createTrackbar('HMax', 'HSV Values', 0, 179, nothing)
    cv2.createTrackbar('SMax', 'HSV Values', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'HSV Values', 0, 255, nothing)

    # Set default value for Max HSV trackbars

    

    # Initialize HSV min/max values
    hMin = h
    sMin = s
    vMin = v

    hMax = hM
    sMax = sM
    vMax = vM

    cv2.setTrackbarPos('HMin', 'HSV Values', h)
    cv2.setTrackbarPos('SMin', 'HSV Values', s)
    cv2.setTrackbarPos('VMin', 'HSV Values', v)

    cv2.setTrackbarPos('HMax', 'HSV Values', hM)
    cv2.setTrackbarPos('SMax', 'HSV Values', sM)
    cv2.setTrackbarPos('VMax', 'HSV Values', vM)

    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    while(1):

        ret, image = cap.read()

        # Get current positions of all trackbars
        
        hMin = cv2.getTrackbarPos('HMin', 'HSV Values')
        sMin = cv2.getTrackbarPos('SMin', 'HSV Values')
        vMin = cv2.getTrackbarPos('VMin', 'HSV Values')
        hMax = cv2.getTrackbarPos('HMax', 'HSV Values')
        sMax = cv2.getTrackbarPos('SMax', 'HSV Values')
        vMax = cv2.getTrackbarPos('VMax', 'HSV Values')

        # Set minimum and maximum HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Convert to HSV format and color threshold
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(image, image, mask=mask)

        # Print if there is a change in HSV value
        if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax)):
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (
                hMin, sMin, vMin, hMax, sMax, vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax
        
        

        # Display result image
        cv2.imshow('tuneHSV', result)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return hMin, sMin, vMin, hMax, sMax, vMax


if __name__ == '__main__':
    h, s, v, hM, sM, vM = tuneHSV(0, 0, 0, 0, 0, 0)
    thresholding(h,s,v,hM,sM,vM)

