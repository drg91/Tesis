#!/usr/bin/env python

import Queue
import threading
import socket
import sys
import time
import os
import cv2gpu
import cv2


#path_capturas = "/home/pi/Tesis/multiplexV2/CapturasFast/"
#path_capturas = "/Users/drg91/Tesis/hiloPy/"

class Proce(threading.Thread):
    def __init__(self, cola):
        threading.Thread.__init__(self)
        self.cola = cola

    def run(self):
        i=0
        comando="./stitching --output resultado"+ repr(i)+".jpg "
        while True:
            msg = self.cola.get()

            comando = comando + msg + " "
            if msg == 'salir':
                print '[Proce]  ' + msg + '\n'
                break

            print '[Proce]  ' + msg + '\n'

            i=i+1
            if (i%4 == 0):
                os.system(comando)
                detectGPU("resultado"+ repr(i)+".jpg ")
                comando="./stitching --output resultado"+ repr(i)+".jpg "


    def detectGPU(archivo):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        image_file = os.path.join(this_dir, archivo)

        cascade_file_cpu = os.path.join(this_dir, 'haarcascade_frontalface_default.xml')
        cascade_file_gpu = os.path.join(this_dir, 'haarcascade_frontalface_default_cuda.xml')

        cv2gpu.init_gpu_detector(cascade_file_gpu)
        print "Se uso GPU"
        faces = cv2gpu.find_faces(image_file)
        image = cv2.imread(image_file)
        for (x, y, w, h) in faces:
            image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imwrite('1' + archivo,image)
        cv2.waitKey(5)


class Recep(threading.Thread):
    def __init__(self, cola):
        threading.Thread.__init__(self)
        self.cola = cola


    def run(self):
        s = socket.socket()
        host = "0.0.0.0"
        port = 9996
        s.bind((host,port))
        s.listen(10)

        i=1
        print "[INFO] Esperando conexion..."
        while True:
            sc, address = s.accept()

            print "[INFO] Conexion con " + str(address)
            nombre_archivo = "vaca" + str(i)+".jpg"

            f = open(nombre_archivo,'wb') #open in binary
            i=i+1

            l = 1
            while(l):
                l = sc.recv(4096)
                while (l):
                    f.write(l)
                    l = sc.recv(4096)
                f.close()
                print "[INFO] Se recibio el archivo: " + nombre_archivo
                self.cola.put(nombre_archivo)
            sc.close()
            print "[INFO] Esperando conexion..."
        s.close()

        self.cola.put('salir')


def test():

    cola =  Queue.Queue()
    proce = Proce(cola)
    recep = Recep(cola)


    proce.start()
    recep.start()

if __name__ == '__main__':
    test()
