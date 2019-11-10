#!/usr/bin/env python

import ivport
import time
import numpy as np
from PIL import Image
import cv2

#path_capturas = "/home/pi/Tesis/v2/multiplexV3/capturasFastTemp/"

def main():
    i = 0
    iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
    iv.camera_open(camera_v2=True, resolution=(800,600))
    while True:


        #start_time = time.time()
        iv.camera_change(1)
        #    iv.framerate = 90
        time.sleep(0.1)
        iv.camera_capture(str(i)+"picam", use_video_port=False)
        #    elapsed_time = time() - start_time
        #    print("Elapsed time: %.10f seconds." % elapsed_time)
        #    start_time = time()
        iv.camera_change(2)
        time.sleep(0.1)
        iv.camera_capture(str(i)+"picam", use_video_port=False)
        #    elapsed_time = time() - start_time
        #    print("Elapsed time: %.10f seconds." % elapsed_time)
        #    start_time = time()
        iv.camera_change(3)
        time.sleep(0.1)
        iv.camera_capture(str(i)+"picam", use_video_port=False)
        #    elapsed_time = time() - start_time
        #    print("Elapsed time: %.10f seconds." % elapsed_time)
        #    start_time = time()
        iv.camera_change(4)
        time.sleep(0.1)
        iv.camera_capture(str(i)+"picam", use_video_port=False)
        #elapsed_time = time.time() - start_time
        #print("Elapsed time: %.10f seconds." % elapsed_time)
        i += 1
        time.sleep(1)

    iv.close()

if __name__ == "__main__":
    main()
