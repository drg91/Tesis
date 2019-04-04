#!/usr/bin/env python

import ivport
import time
import numpy as np
from PIL import Image

path_capturas = "/home/pi/Tesis/Tesisv2/tesis/multiplexV2/CapturasFast/"
path_unidas = "/home/pi/Tesis/Tesisv2/tesis/multiplexV2/UnidasFast/"

def unir(img1,img2,img3,img4,imgSalida):
    images_list = [path_capturas+ img1+'.jpg',path_capturas+img2+'.jpg',path_capturas+img3+'.jpg',path_capturas+img4+'.jpg']
    imgs = [ Image.open(i) for i in images_list ]
    imgs[0]= imgs[0].rotate(180)
    img_merge = np.hstack( (np.asarray( i ) for i in imgs ) )
    img_merge = Image.fromarray( img_merge)
    img_merge.save(path_unidas+ imgSalida + time.strftime("%y%m%d_%H-%M-%S") + '.jpg', "JPEG",optimize=True, quality=100)
    print "Imagenes Unidas: "+img1 + " "+img2+ " "+img3+ " "+img4

def main():

    iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
    iv.camera_open(camera_v2=True, resolution=(640,480))
    iv.camera_change(1)
    iv.camera_capture(path_capturas+"picam", use_video_port=False)
    #time.sleep(0.4)
    iv.camera_change(2)
    iv.camera_capture(path_capturas+"picam", use_video_port=False)
    #time.sleep(0.4)
    iv.camera_change(3)
    iv.camera_capture(path_capturas+"picam", use_video_port=False)
    #time.sleep(0.4)
    iv.camera_change(4)
    iv.camera_capture(path_capturas+"picam", use_video_port=False)

    unir('picam_CAM1','picam_CAM2','picam_CAM3','picam_CAM4','picam_Unida')
    #time.sleep(0.8)

    iv.close()

if __name__ == "__main__":
    main()
