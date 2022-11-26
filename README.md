# Modulo: INTEGRACIÓN DE LA ROBÓTICA Y AUTOMATIZACIÓN

Este proyecto fue desarrollado con Ubuntu 20.04 y ROS Noetic.

## Compilación
Despues de clonar este repositorio en un workspace de ROS, compilelo con:

```
catkin_make
```
No olvide actualizar la terminal con:
```
source devel/setup.bash
```
## Ejecución

Se dividio el proyecto para que corra con 3 terminales diferentes:<br />
Una para gazebo, otra para YOLOv5, Y otra para el proyecto. <br />
De esta manera, es mas rapido evaluar diferentes parametros para cada escenario, siendo que se puede dejar corriendo las terminales más pesadas (Gazebo, Yolo) y cambiar los parametros del proyecto.

Se a creado archivos bash que simplifican la ejecucion de los comandos del proyecto.<br />
En este sentido, debera mover los 3 archivos de la carpeta "comandos" fuera del src del workspace. <br />
Y debe hacerlos ejecutables. Ver imagen de referencia:

![image](https://user-images.githubusercontent.com/74274632/204111662-c9a1d678-5cdf-45d7-9131-7bb7c2466e8f.png)

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
project.sh A
```

En este caso el parametro "A" indica el objetivo del brazo respecto a:.

![image](https://user-images.githubusercontent.com/74274632/204111977-ef9fb0ed-f6c7-473b-8b6e-4f60d3396189.png)


## Demostraciones
