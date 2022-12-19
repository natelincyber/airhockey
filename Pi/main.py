import os, serial
import cv2
import numpy as np
import threading

cameraPort = 1

lowThresh = [52, 0, 0]
highThresh = [91, 255, 255]
kernel = np.ones((5,5),np.uint8)
minArea = 500
camera = None

def connectToArduino():
    os.system("cls" if os.name == 'nt' else 'clear')
    print("[INFO] Establishing serial connection to arduino")

    maxPorts = 9

    for port in range(maxPorts):
        try:
            print(f'[INFO] Connecting to COM{port}')
            arduino = serial.Serial(port=f'COM{port}', baudrate=115200, timeout=.1)
            if arduino:
                print("[INFO] Connected")
                return arduino
            
        except serial.serialutil.SerialException:
            continue
    
def dataHandler(arduino, x,y):
  
    send = f"{str(x)}|{str(y)}"


    try:
        arduino.write(bytes(send, 'utf-8'))
    except serial.serialutil.SerialException:
        print("[ERROR] Lost connection to Arduino")
        exit()

def openCamera():
    print('[INFO] opening camera')
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    r, frame = cap.read()
    print("[INFO] camera stream started")
    print('Resolution: ' + str(frame.shape[0]) + ' x ' + str(frame.shape[1]))

    return cap



def detectObject(cap):


    ret, image = cap.read(cameraPort)

    # Set upper and lower bounds
    lower = np.array(lowThresh)
    upper = np.array(highThresh)

    # Convert to HSV format and color threshold
    filter = cv2.bilateralFilter(image, 10, 80, 80)
    hsv = cv2.cvtColor(filter, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    # clean up the image before processing
    ret, th1 = cv2.threshold(
            mask, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    th2 = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)

    # detect contours
    contours, hierarchy = cv2.findContours(th2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    x = 0
    y = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > minArea:
            cv2.drawContours(image, contour, -1, (0,255,0))
            rect = cv2.boundingRect(contour)
            x,y,w,h = rect
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(image,f'Object @ ({x+w/2},{y+h/2})',(x,y+h+10),0,0.3,(0,255,0))

            # coordinates of object
            x = x+w/2
            y = y+h/2

    cv2.imshow('image', image)
    if cv2.waitKey(1) == 27:
        return


    return x, y 

def waitForReady(arduino):
    print('[INFO] waiting for arduino')
    while True:
        try:
            if str(arduino.readline().decode()) == "ready":
                break
            else:
                continue
        except:
            continue


if __name__ == '__main__':

    arduino = connectToArduino()
    camera = openCamera()

    waitForReady(arduino)
    print('[INFO] arduino ready')

    while True:
        x,y = detectObject(camera)
        dataHandler(arduino, x, y)
    
