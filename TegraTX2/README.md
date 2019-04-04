# Tesis de grado FCEFyN Ing Computacion

#### Garbiglia Diego Rodrigo
 
## Habilitar Denver2 (Arm especifico de NVIDIA - 2 Cores -)

```shell
  nvidia@tegra-ubuntu:~$ ~/tegrastats
  RAM 970/7854MB (lfb 1546x4MB) cpu [0%@2035,off,off,0%@2035,0%@2035,0%@2035]
  RAM 971/7854MB (lfb 1546x4MB) cpu [0%@2035,off,off,1%@2035,0%@2035,0%@2035]
  RAM 971/7854MB (lfb 1546x4MB) cpu [0%@2035,off,off,1%@2035,0%@2035,0%@2035]
```
Se observar que hay dos apagados, el core 1 y 2

Existe la posibilidad de habilitarlos por sysfs

```shell
  nvidia@tegra-ubuntu:~$ sudo su
  root@tegra-ubuntu:/home/nvidia# echo 1 > /sys/devices/system/cpu/cpu1/online
  root@tegra-ubuntu:/home/nvidia# echo 1 > /sys/devices/system/cpu/cpu2/online
```
Chequeamos que se activen

```shell
  nvidia@tegra-ubuntu:~$ ~/tegrastats
  RAM 973/7854MB (lfb 1545x4MB) cpu [0%@2035,0%@345,0%@345,0%@2035,0%@2035,0%@2035]
  RAM 973/7854MB (lfb 1545x4MB) cpu [1%@2035,1%@345,1%@345,0%@2035,0%@2035,0%@2035]
  RAM 973/7854MB (lfb 1545x4MB) cpu [0%@2035,0%@345,0%@345,0%@2035,0%@2035,1%@2035]
```
Tambien se le pueden aumentar la frecuencia a esos cores que activamos

```shell
nvidia@tegra-ubuntu:~$ sudo ./jetson_clocks.sh
[sudo] password for nvidia:

nvidia@tegra-ubuntu:~$ ~/tegrastats
RAM 979/7854MB (lfb 1545x4MB) cpu [0%@2035,0%@2419,0%@2419,0%@2035,0%@2035,0%@2035]
RAM 979/7854MB (lfb 1545x4MB) cpu [1%@2035,0%@2419,0%@2419,0%@2035,0%@2035,0%@2035]
RAM 979/7854MB (lfb 1545x4MB) cpu [0%@2035,0%@2419,0%@2419,0%@2035,0%@2035,0%@2035]
```

Como otra posibilidad para habilitarlos y para ver los modos en que se pueden setear la TX2

Para listar todos los modos y mas informacion
```shell
nvidia@tegra-ubuntu:~$ nvpmodel -p --verbose
```
Para setear el modo 2 que habilita MAXP de todos los cores
```shell
nvidia@tegra-ubuntu:~$ nvpmodel -m 2
```


###### by drg91
