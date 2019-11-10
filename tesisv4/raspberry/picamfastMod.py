#!/usr/bin/env python

from time import time
import picamera
import picamera.array
import cv2
import IIC
import RPi.GPIO as gp
gp.setwarnings(False)
gp.setmode(gp.BOARD)

start_time = time()

iviic = IIC.IIC(addr=(0x70), bus_enable =(0x01))
fPin = f1Pin = f2Pin = ePin = 0
IVJP = {'A': (11, 12), 'C': (21, 22), 'B': (15, 16), 'D': (23, 24)}
f1Pin, f2Pin = IVJP['A']
ePin = 7
gp.setup(f1Pin, gp.OUT)
gp.setup(f2Pin, gp.OUT)
gp.setup(ePin, gp.OUT)
iviic.write_control_register((0x01))
gp.output(ePin, False)
gp.output(f1Pin, False)
gp.output(f2Pin, True)

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 8
    camera.start_preview()
    #    time.sleep(2)
    with picamera.array.PiRGBArray(camera) as stream:
        i=1
        camera.capture(stream, format='bgr')
        # At this point the image is available as stream.array
        image = stream.array
image = image[:, :, ::-1]
#cv2.imshow('image',image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
iviic.write_control_register((0x02))
gp.output(ePin, True)
gp.output(f1Pin, False)
gp.output(f2Pin, True)
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 8
    camera.start_preview()
    with picamera.array.PiRGBArray(camera) as stream:
        i=1
        camera.capture(stream, format='bgr')
# At this point the image is available as stream.array
        image2 = stream.array
image2 = image2[:, :, ::-1]
iviic.write_control_register((0x04))
gp.output(ePin, False)
gp.output(f1Pin, True)
gp.output(f2Pin, False)
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 8
    camera.start_preview()
    with picamera.array.PiRGBArray(camera) as stream:
        i=1
        camera.capture(stream, format='bgr')
    # At this point the image is available as stream.array
        image3 = stream.array
image3 = image3[:, :, ::-1]
iviic.write_control_register((0x08))
# gp.output(ePin, True)
gp.output(f1Pin, True)
gp.output(f2Pin, False)
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 8
    camera.start_preview()
    with picamera.array.PiRGBArray(camera) as stream:
        i=1
        camera.capture(stream, format='bgr')
# At this point the image is available as stream.array
        image4 = stream.array
image4 = image4[:, :, ::-1]

elapsed_time = time() - start_time
print("Elapsed time: %.10f seconds." % elapsed_time)
#cv2.imshow('image',image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
