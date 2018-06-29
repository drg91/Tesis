# Tesis de grado FCEFyN Ing Computacion

#### Garbiglia, Diego Rodrigo

## Software en C++ para deteccion de caras y ojos, usa OpenCV 3.3.0.

### Configuracion previa:

Se carga un modulo de kernel en la raspberry

```shell
sudo modprobe bcm2835-v4l2
```

### Compilacion:

```shell
cmake .
make
```

### Ejecucion:

```shell
./facedetect
```

