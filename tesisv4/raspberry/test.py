import time
import picamera
import picamera.array
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


with picamera.PiCamera() as camera:
    # camera.start_preview()
    camera.resolution=(640,480)
    camera.framerate=30
    time.sleep(2)
    i=2
    with picamera.array.PiRGBArray(camera) as rawCapture:
        time.sleep(0.1)
        start = time.time()
        for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
            image=frame.array
            #cv2.imshow("Video Feed", image)
            cv2.imwrite((str(i) + "test.jpg"), image );
            if i>4:
                i=1
                elapsed_time = time.time() - start
                print("Elapsed time: %.10f seconds." % elapsed_time)
                break
            camera_change(i)
            i=i+1
            #key=cv2.waitKey(1) & 0xff
            rawCapture.truncate(0)
            #if key==ord("q"):
            #    break
