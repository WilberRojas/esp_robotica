# Modulo: INTEGRACIÓN DE LA ROBÓTICA Y AUTOMATIZACIÓN

Este proyecto fue desarrollado con Ubuntu 20.04 y ROS Noetic.

## Clonación
Se debe clonar este branch dentro de un workspace de ROS.<br />
Para clonar este branch use:
```
git clone https://github.com/WilberRojas/esp_robotica -b integracion
```
compilar con:
```
catkin_make
```

## Ejecución

Se dividio el proyecto para que corra con 4 terminales diferentes:<br />
Una para gazebo, otra para YOLOv5, otra para el proyecto, y otra para el trigger. <br />
De esta manera, es más rápido evaluar diferentes parametros para cada escenario, siendo que se puede dejar corriendo las terminales más pesadas (Gazebo, Yolo) y cambiar el objetivo del brazo.

Se a creado archivos bash que simplifican la ejecucion de los comandos del proyecto.<br />
En este sentido, debera mover los 3 archivos de la carpeta [comandos](/comandos) fuera del src del workspace. <br />
Y debe hacerlos ejecutables. Ver imagen de referencia:

![image](https://user-images.githubusercontent.com/74274632/204111662-c9a1d678-5cdf-45d7-9131-7bb7c2466e8f.png)

> Nota: Hay que descomprimir el package de yolo en la carpeta [class_pkgs](/class_pkgs).  <br />
Los cambios en estos packages se encuentran detallados en el [README.md](/class_pkgs/README.md) de la misma carpeta  <br />
En resumen se tiene esta estructura de packages: <br />
![image](https://user-images.githubusercontent.com/74274632/204145978-950fe188-f8b1-47d1-942c-edb1580c86b2.png)

### Terminal 1:
Primero corremos el mundo de gazebo con:
```
./gazebo.sh A
```
En donde el parametro "A" indica el escenario que se desea correr.

### Terminal 2:
Ahora correremos Yolo, el cual necesita que gazebo este en ejecucion ya que usa la camara del robot:
```
./yolo.sh
```
### Terminal 3:
Ahora correremos el proyecto:
```
./project.sh goalA
```

En este caso el parametro "goalA" indica el objetivo del brazo respecto a:.

![image](https://user-images.githubusercontent.com/74274632/204111977-ef9fb0ed-f6c7-473b-8b6e-4f60d3396189.png)

### Terminal 4:
Finalmente le mandamos la señal al kuka para que se mueva:
```
rostopic pub /trigger std_msgs/Int32 "data: 1"
```
## Demostraciones

https://user-images.githubusercontent.com/74274632/204146264-fd2c58c4-1c5b-4761-bae4-d736b0524cf9.mp4

https://user-images.githubusercontent.com/74274632/204146348-b8bcd6eb-9154-4f5b-a51d-ef1fa874ae51.mp4

https://user-images.githubusercontent.com/74274632/204146358-213086c4-3b11-4a37-840b-707bf8995d1f.mp4

https://user-images.githubusercontent.com/74274632/204146363-32ae43b3-70f8-4392-ade5-366d4b037f85.mp4
