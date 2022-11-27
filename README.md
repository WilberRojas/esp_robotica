# Modulo: INTEGRACIÓN DE LA ROBÓTICA Y AUTOMATIZACIÓN

Este proyecto fue desarrollado con Ubuntu 20.04 y ROS Noetic.

## Clonación
Se debe clonar este branch dentro del src de un workspace de ROS.<br />
Para clonar este branch use:
```
git clone https://github.com/WilberRojas/esp_robotica -b integracion
```
Ahora debe hacer ejecutable el archivo setup.sh y correrlo, ver imagen para referencia.
En resumen, setup.sh hara:
* Ejecutables los archivos .py
* Moverá y hara ejecutables los archivos de la carpeta comandos (que se usan en las terminales después)
* Descomprimirá los packages de yolo
* Compilará el proyecto

![image](https://user-images.githubusercontent.com/74274632/204157841-931b3b0e-be6b-4018-a24d-1ad73f63208b.png)

> Nota: Los cambios de los packages de clases en [README.md](/class_pkgs/README.md) 

En resumen se tiene esta estructura de packages: <br />
![image](https://user-images.githubusercontent.com/74274632/204158739-afa57274-d400-45a0-a1b2-70c463091059.png)


## Ejecución

Se dividio el proyecto para que corra con 4 terminales diferentes:<br />
 * Una para gazebo
 * Otra para YOLO
 * Otra para el proyecto
 * Y otra para el trigger. 
 
De esta manera, es más rápido evaluar diferentes parametros para cada escenario, siendo que se puede dejar corriendo las terminales más pesadas (Gazebo, Yolo) y cambiar el objetivo del brazo.

Si corrio setup.sh entonces notara que hay 3 archivos fuera del src del workspace, ver imagen de referencia:

![image](https://user-images.githubusercontent.com/74274632/204158147-614b2c75-72c4-42c8-b21d-7e27e726fe17.png)

Habra 4 terminales dentro de su "ros_ws" y corra:

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
