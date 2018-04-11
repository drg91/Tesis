# Tesis de grado FCEFyN Ing Computacion

Garbiglia Diego Rodrigo

### Instalacion

Primero hay que activar I2C desde raspi-config, [usar este link](http://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi)

Y activar el modulo de la camara desde raspi-config.

### Clonar el repositorio

```shell
git clone https://github.com/drg91/Tesis.git
```

### Instalacion de dependencias

```shell
sudo apt-get install python-smbus
```
Como el modulo de picamera usado en este repositorio es un fork del original https://github.com/waveform80/picamera se edito para que funcione con la version 2 de la camaras y soporte la placa multiplexadora IVport. Hay que desinstalar el picamera que viene en el Raspbian.


```shell
sudo apt-get remove python-picamera
sudo pip uninstall picamera
```

###Uso

First of all it is important that **init_ivport.py** should be run at every boot before starting to access camera.

```shell
cd ivport-v2
python init_ivport.py
```

And check whether ivport and camera are detected by raspberry pi or no with **vcgencmd get_camera**.

```shell
root@ivport:~/ivport-v2 $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: 10 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- 64 -- -- -- -- -- -- -- -- -- -- -- 
70: 70 -- -- -- -- -- -- --
```
You should get both **0x70** and **0x64** as addresses of respectively **ivport v2** and **camera module v2**.

```shell
root@ivport:~/ivport-v2 $ vcgencmd get_camera
supported=1 detected=1
```
**supported** and **detected** should be **1** before **test_ivport.py** script.

There is **test_ivport.py** script for **IVPORT DUAL V2**.

```python
import ivport
# raspistill capture
def capture(camera):
    "This system command for raspistill capture"
    cmd = "raspistill -t 10 -o still_CAM%d.jpg" % camera
    os.system(cmd)

iv = ivport.IVPort(ivport.TYPE_DUAL2)
iv.camera_change(1)
capture(1)
iv.camera_change(2)
capture(2)
iv.close()
```
**TYPE** and **JUMPER** settings are configured while initialize ivport.
```python
ivport.IVPort(IVPORT_TYPE, IVPORT_JUMPER)
```
**RESOLUTION**, **FRAMERATE** and other settings can be configured.
```python
iv = ivport.IVPort(ivport.TYPE_DUAL2)
iv.camera_open(camera_v2=True, resolution=(640, 480), framerate=60)
```
Also **init_ivport.py** should be run at every boot before starting to access camera.

```shell
cd ivport-v2
python init_ivport.py
```

Tests
------

There is **test_ivport.py** script which is for testing. 
```shell
cd ivport-v2
python test_ivport.py
```
