from ctypes import *
import math
import random
import cv2
import numpy as np
import time
import datetime

path_capturas = "imagenes/"

def sample(probs):
    s = sum(probs)
    probs = [a / s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs) - 1


def c_array(ctype, values):
    arr = (ctype * len(values))()
    arr[:] = values
    return arr


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


lib = CDLL("libdetector.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)


def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res


def get_angle(b, a):
    myradians = math.atan2(a[1]-b[1], a[0]-b[0])
    mydegrees = math.degrees(myradians)
    return mydegrees*-1


def switch_polar_ned(angle):
    if angle < 0 or angle >= 360:
        while angle < 0:
            angle = angle + 360
        while angle >= 360:
            angle = angle - 360

    if angle <= 90:
        return 90 - angle
    else:
        return 450 - angle


def detect(filtroIn, id, flag, net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = load_image(image, 0, 0)
    num = c_int(0)
    pnum = pointer(num)
    predict_image(net, im)
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    filtro = 0
    if (nms): do_nms_obj(dets, num, meta.classes, nms);
    if flag:
        img = cv2.imread(image, 3)
    if filtroIn:
        filtro = 0.8
    res = []
    sizeDetect = 0.0
    width = 0.0
    height = 0.0

    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > filtro:
                b = dets[j].bbox

                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
                if flag:
                    height = np.size(img, 0)
                    width = np.size(img, 1)
                    # print "h: ", height
                    # print "w: ", width

                    w1 = int(b.w / 2)
                    h1 = int(b.h / 2)
                    x1 = int(b.x)
                    y1 = int(b.y)

                    cv2.circle(img, (x1, y1), 5, (255, 255, 120))
                    # cv2.circle(img, ((width / 2), (height / 2)), 5, (0, 255, 255))
                    cv2.circle(img, ((width / 2), height), 5, (0, 255, 255))
                    angulo = get_angle(((width / 2), height), (x1, y1))
                    print("Angulo: ", angulo, " grados")
                    print("NED: ", switch_polar_ned(angulo))
                    cv2.rectangle(img, ((x1 - w1), (y1 - h1)), (x1 + w1, (y1 + h1)), (0, 255, 0), 2)
                    cv2.line(img, (x1, y1), ((width / 2), height), (255, 255, 0), 2)

                    # cv2.line(img, (width, 0), ((width / 2), height), (255, 255, 0), 2)
                    tiempo = time.time()
                    st = datetime.datetime.fromtimestamp(tiempo).strftime('%d-%m-%YY-%H:%M:%S')
                    nombre_archivo = path_capturas + "proce" + st + ".jpg"
                    cv2.putText(img,meta.names[i], (x1 + w1, y1 + h1), 0, 2, 255, 2)
                    cv2.imwrite(nombre_archivo,img)
                    #cv2.imshow("Tesis", img)
                    #tecla = cv2.waitKey(0)

    try:
        res = sorted(res, key=lambda x: -x[1])
        res = res[0]
    except IndexError:
        res = res

    free_image(im)
    free_detections(dets, num)
    return res


if __name__ == "__main__":
    # net = load_net("cfg/densenet201.cfg", "/home/pjreddie/trained/densenet201.weights", 0)
    # im = load_image("data/wolf.jpg", 0, 0)
    # meta = load_meta("cfg/imagenet1k.data")
    # r = classify(net, meta, im)
    # print r[:10]
    net = load_net("cfg/yolov3-tiny.cfg", "yolov3-tiny.weights", 0)
    meta = load_meta("cfg/coco.data")
    r = detect(0, 0, 1, net, meta, "stit10.jpg")
    print r
