import os, cv2
import serial


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
    
def dataHandler(arduino, data):
    send = data
    try:
        arduino.write(bytes(send, 'utf-8'))
    except serial.serialutil.SerialException:
        print("[ERROR] Lost connection to Arduino")
        exit()




if __name__ == '__main__':
    arduino = connectToArduino()
    while True:
        inp = input("send ")
        dataHandler(arduino, inp)
