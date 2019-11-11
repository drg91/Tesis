#!/usr/bin/env python
# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
import sys

def main():
    stitcher = cv.createStitcher(False)

    # read input images
    imgs = []
    imagenes = ["recep1.jpg","recep2.jpg","recep3.jpg","recep4.jpg"]
    for img_name in imagenes:
        img = cv.imread(img_name)
        if img is None:
            print("can't read image " + img_name)
            sys.exit(-1)
        imgs.append(img)


    status, pano = stitcher.stitch(imgs)

    if status != cv.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
        sys.exit(-1)

    cv.imwrite("test.jpg", pano);
    print("stitching completed successfully")

    print('Done')


if __name__ == '__main__':
    main()
    cv.destroyAllWindows()
