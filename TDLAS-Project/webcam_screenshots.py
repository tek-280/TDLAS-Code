from cv2 import *
import time

filepath= r"C:\Users\vaclab\Desktop\TDLAS-Project\Screenshots\\"
cap = VideoCapture(0)   # 0 -> index of camera
cap.set(3,1280)
cap.set(4,1024)
cap.set(10, 0.0001)
try:
    while True:
        s, img = cap.read()
        if s:    # frame captured without any errors
            waitKey(0)
            imwrite( filepath +  time.strftime("%Y-%m-%d")+"_TIME_"+time.strftime("%H-%M-%S")+"_Camera_screenshot.jpg",img) #save image
            print(time.strftime("%H-%M-%S")+"screenshot taken!")
            time.sleep(600)
except KeyboardInterrupt:
        print('Stopped by user')
        Newport.set_current(0)
        sys.exit(0)