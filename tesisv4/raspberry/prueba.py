import time
import picamera
import IIC
import RPi.GPIO as gp
gp.setwarnings(False)
gp.setmode(gp.BOARD)


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
    camera.resolution = (1024, 768)
    camera.framerate = 30
    camera.start_preview()
    # Give the camera some warm-up time
#    time.sleep(2)
    start = time.time()
    camera.capture_sequence([
        'image%02d.jpg' % i
        for i in range(frames) if i<4 camera_change(i+1)
        ], use_video_port=True)
    finish = time.time()
print('Captured %d frames at %.2ffps' % (
    frames,
    frames / (finish - start)))

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
