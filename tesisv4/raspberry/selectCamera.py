#!/usr/bin/env python

import ivport
import os

def main():

    iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
    iv.camera_open(camera_v2=True, resolution=(800,600))
    iv.camera_change(3)
    iv.camera_capture("test", use_video_port=False)

    iv.close()

if __name__ == "__main__":
    main()
