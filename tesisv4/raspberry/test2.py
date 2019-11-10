
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import IIC
import RPi.GPIO as gp
gp.setwarnings(False)
gp.setmode(gp.BOARD)

def camera_change(camera=1):
        if camera == 1:
            iviic.write_control_register((0x01))
            gp.output(ePin, False)
            gp.output(f1Pin, False)
            gp.output(f2Pin, True)
        elif camera == 2:
            iviic.write_control_register((0x02))
            gp.output(ePin, True)
            gp.output(f1Pin, False)
            gp.output(f2Pin, True)
        elif camera == 3:
            iviic.write_control_register((0x04))
            gp.output(ePin, False)
            gp.output(f1Pin, True)
            gp.output(f2Pin, False)
        elif camera == 4:

            iviic.write_control_register((0x08))
            gp.output(ePin, True)
            gp.output(f1Pin, True)
            gp.output(f2Pin, False)

frames = 60
iviic = IIC.IIC(addr=(0x70), bus_enable =(0x01))
fPin = f1Pin = f2Pin = ePin = 0
IVJP = {'A': (11, 12), 'C': (21, 22), 'B': (15, 16), 'D': (23, 24)}
f1Pin, f2Pin = IVJP['A']
ePin = 7
gp.setup(f1Pin, gp.OUT)
gp.setup(f2Pin, gp.OUT)
gp.setup(ePin, gp.OUT)

camera_change(1)
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
Capture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)
i=1
# capture frames from the camera
for frame in camera.capture_continuous(Capture, format="bgr", use_video_port=True):
    image = frame.array

    # show the frame and do stuff to it here
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    if i>4:
        i=1
    camera_change(i)
    # clear the stream in preparation for the next frame
    Capture.truncate(0)
    i=i+1
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
