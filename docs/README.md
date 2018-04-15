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

### Uso

Hay que ejecutar **init_ivport.py** cada vez que bootea la placa para poder tener acceso a las camaras.

```shell
cd multiplexV2
python init_ivport.py
```
Y chequear que la raspberry detecta a la placa ivport y a la camara. Ejecutando:
```shell
vcgencmd get_camera
```

```shell
root@raspCam:~/multiplexV2 $ i2cdetect -y 1
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
Se deberia obtener **0x70** y **0x64** en las direcciones respectivamente **ivport v2** y **camera module v2**.

```shell
root@ivport:~/ivport-v2 $ vcgencmd get_camera
supported=1 detected=1
```
**supported** y **detected** deberian ser **1** despues ejecutar **test_ivport.py** script.

Ejemplo del script **test_ivport.py** para la **IVPORT DUAL V2**.

```python
import ivport
# raspistill capture
def capture(camera):
    "Se ejecutara la aplicacion raspistill de raspberry"
    cmd = "raspistill -t 10 -o still_CAM%d.jpg" % camera
    os.system(cmd)

iv = ivport.IVPort(ivport.TYPE_QUAD2)
iv.camera_change(1)
capture(1)
iv.camera_change(2)
capture(2)
iv.camera_change(3)
capture(3)
iv.camera_change(4)
capture(4)
iv.close()
```
**TYPE** y **JUMPER** Son las configuraciones que se setean en el constructor de ivport.

```python
ivport.IVPort(IVPORT_TYPE, IVPORT_JUMPER)
```
**RESOLUTION**, **FRAMERATE** otras de las configuraciones que se pueden modificar.

```python
iv = ivport.IVPort(ivport.TYPE_DUAL2)
iv.camera_open(camera_v2=True, resolution=(640, 480), framerate=60)
```
Ejecutar **init_ivport.py** .

```shell
cd ivport-v2
python init_ivport.py
```

Pruebas
------

Ejecutar **test_ivport.py** .
```shell
cd ivport-v2
python test_ivport.py
```
