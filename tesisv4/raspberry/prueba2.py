import time
import picamera
import IIC
import RPi.GPIO as gp
gp.setwarnings(False)
gp.setmode(gp.BOARD)

def filenames():
    frame = 0
    i=1
    while frame < frames:
        camera_change(i)
        yield 'image%02d.jpg' % frame
        frame += 1
        if i>4:
            i=1
        time.sleep(0.08)
        #camera_change(i)
        i=i+1


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

frames = 5
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
    camera.resolution = (800, 600)
    camera.framerate = 30
    camera.start_preview()
    # Give the camera some warm-up time
    time.sleep(2)
    start = time.time()
    camera.capture_sequence(filenames(), use_video_port=True)
    finish = time.time()
    print('Captured %d frames at %.2f segundos' % (
    frames,
    (finish - start)))
