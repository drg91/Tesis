# Tesis de grado FCEFyN Ing Computacion

#### Garbiglia Diego Rodrigo

## Instalacion de OpenCV 3.3.0 en Raspberry 3 model B

### Instalacion de dependencias

```shell
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python2.7-dev python3-dev
```

### Descargar el codigo fuente de OpenCV

```shell
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.3.0.zip
unzip opencv.zip
```
Para tener acceso a los modulos de SIFT y SURF (Descriptores para detectores de puntos y features)
hay que descargar el codigo fuente de *opencv_contrib*

```shell
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.3.0.zip
$ unzip opencv_contrib.zip
```

### Python 2.7 o 3?

Es necesario elegir la version para instalar el PIP, pueden ser ambas versiones.


```shell
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo python3 get-pip.py
```

### Instalar numpy, libreria necesaria

```shell
pip install numpy
```

### Compilar e instalar OpenCV

```shell
cd ~/opencv-3.3.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    -D BUILD_EXAMPLES=ON ..
```
### Chequear el resultado del cmake

https://www.pyimagesearch.com/wp-content/uploads/2017/09/py27_cv.png

### Modificar el tamanio del la memoria SWAP

Cambiando el valor de la variable *CONF_SWAPSIZE* en el archivo _/etc/dphys-swapfile_

```shell
# CONF_SWAPSIZE=100
CONF_SWAPSIZE=1024
```
Para que tome el nuevo valor hay que reiniciar el servicio de *dphys-swapfile*

```shell
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
```

Compilar con 4 hilos por los 4 cores que tiene las Raspberry

```shell
make -j4
```

Y finalmente instalar

```shell
sudo make install
sudo ldconfig
```

### Chequear que la instalacion termino correctamente y se puede visualizar la libreria.

#### Para python 2.7

```shell
ls -l /usr/local/lib/python2.7/site-packages/
total 1852
-rw-r--r-- 1 root staff 1895772 Mar 20 20:00 cv2.so
```

### Test

```shell
source ~/.profile
workon cv
python
>>> import cv2
>>> cv2.__version__
'3.3.0'
>>>
```
### Eliminar archivos source de compilacion

```shell
rm -rf opencv-3.3.0 opencv_contrib-3.3.0
```

## NO OLVIDAR! volver al tamanio original el valor de la variable *CONF_SWAPSIZE* en el archivo _/etc/dphys-swapfile_

```shell
CONF_SWAPSIZE=100
#CONF_SWAPSIZE=1024
```
Para que tome el nuevo valor hay que reiniciar el servicio de *dphys-swapfile*

```shell
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
```

## Listo

###### by drg91
