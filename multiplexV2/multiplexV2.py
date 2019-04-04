#!/usr/bin/env python

import os
import ivport
import time
import numpy as np
from PIL import Image

path_capturas = "/home/pi/Tesis/Tesisv2/tesis/multiplexV2/Capturas/"
path_unidas = "/home/pi/Tesis/Tesisv2/tesis/multiplexV2/ImagenesUnidas/"

def picam_sequence():
    FRAMES = 30
    CAM = 0
    def sequence_outputs(iv):
        frame = 0
        while frame < FRAMES:
            camera = (frame%4)+1
            time.sleep(0.2)   # SD Card Bandwidth Correction Delay
            iv.camera_change(camera)
            time.sleep(0.2)   # SD Card Bandwidth Correction Delay
            yield path_capturas+'sequence_%02d.jpg' % frame
            frame += 1
            print camera

    iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
    iv.camera_open(camera_v2=True, resolution=(640, 480), framerate=60)
    #iv.picam.resolution = (640, 480)
    #iv.picam.framerate = 30
    time.sleep(1)
    iv.camera_sequence(outputs=sequence_outputs(iv), use_video_port=True)
    iv.close()

def picam_capture():
    iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
    iv.camera_open(camera_v2=True, resolution=(1024, 768))
    FRAMES2 = 10
    frame = 0

    while frame < FRAMES2:
        iv.camera_change(1)
        iv.camera_capture(path_capturas+str(frame)+"picam", use_video_port=False)
        #time.sleep(0.4)
        iv.camera_change(2)
        iv.camera_capture(path_capturas+str(frame)+"picam", use_video_port=False)
        #time.sleep(0.4)
        iv.camera_change(3)
        iv.camera_capture(path_capturas+str(frame)+"picam", use_video_port=False)
        #time.sleep(0.4)
        iv.camera_change(4)
        iv.camera_capture(path_capturas+str(frame)+"picam", use_video_port=False)

        unir(str(frame)+'picam_CAM1',str(frame)+'picam_CAM2',str(frame)+'picam_CAM3',str(frame)+'picam_CAM4',str(frame)+'picam_Unida')
        frame += 1
        #time.sleep(0.8)

    iv.close()


def still_capture():
    # raspistill capture
    def capture(camera):
        "This system command for raspistill capture"
        cmd = "raspivid -o vid%d.h264" % camera
        os.system(cmd)

    iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
    iv.camera_change(1)
    capture(1)
    iv.camera_change(2)
    capture(2)
    iv.camera_change(3)
    capture(3)
    iv.camera_change(4)
    capture(4)
    iv.close()
    #unir('still_CAM1','still_CAM2','still_CAM3','still_CAM4','still_Unida')

def unir(img1,img2,img3,img4,imgSalida):
    images_list = [path_capturas+ img1+'.jpg',path_capturas+img2+'.jpg',path_capturas+img3+'.jpg',path_capturas+img4+'.jpg']
    imgs = [ Image.open(i) for i in images_list ]
    imgs[0]= imgs[0].rotate(180)
    img_merge = np.hstack( (np.asarray( i ) for i in imgs ) )
    img_merge = Image.fromarray( img_merge)
    img_merge.save(path_unidas+ imgSalida + time.strftime("%y%m%d_%H-%M-%S") + '.jpg' )
    print "Imagenes Unidas: "+img1 + " "+img2+ " "+img3+ " "+img4

def hacer_nada():
    pass

def main():
    #still_capture()
    #picam_capture()
    #picam_sequence()

    acciones = {"1": still_capture, "2": picam_capture, "3": picam_sequence}
    while True:
        print "Opciones: 1)still_capture 2)picam_capture 3)picam_sequence *q para salir*"
        seleccion = raw_input("Opcion: ")
        if "q" == seleccion:
            print "Saliendo..."
            return
        toDo = acciones.get(seleccion, hacer_nada)
        toDo()

if __name__ == "__main__":
    main()
