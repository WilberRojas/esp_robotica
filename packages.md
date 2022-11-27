# Cambios en los packages de clases
1. aruco_pose

Se añadio dos archivos launch, uno busca el aruco 17 y otro el aruco 29. </br>
Esto con el objetivo de llamarlos desde un launch, ya que se encontro problemas al pasarle desde un launch el parametro "markerId".

![image](https://user-images.githubusercontent.com/74274632/204141998-b5b984e1-7890-4ab9-828c-2ce52f53095f.png)

2. percepcion

El moveit desarrollado desde 0, retorna este error al correrlo junto a los test de gazebo

![image](https://user-images.githubusercontent.com/74274632/204142167-13d1b8c2-74dd-4ea0-af04-a17f597a8a1d.png)

Por lo que se cambio el archivo urdf del robot diferencial como se muestra a continuacion:

![image](https://user-images.githubusercontent.com/74274632/204142845-504ee33c-868f-45e5-b83e-de804fef7836.png)

Esto para ambas ruedas del robot.

4. Yolo

Un cambio minimo se aplico, Yolo ya no despliega la ventana de imagen, en su lugar se configuro el RVIZ para que la muestre.

![image](https://user-images.githubusercontent.com/74274632/204142272-f6b985aa-b318-4590-81ac-069e58ad259e.png)

6. Moveit comander

Este package corresponde a Moveit y fue modificado para eliminar el siguiente warning.

![image](https://user-images.githubusercontent.com/74274632/204142435-6f1a3689-bc8e-4bbc-b050-c0aa18bef117.png)

Se modifico el codigo de planing_scene_interface.py como se muestra a continuacion:

![image](https://user-images.githubusercontent.com/74274632/204142573-675174ac-cc94-4dfe-bb7c-e28cc6bbeae3.png)


Se obtuvo la solucion de: https://github.com/ros-planning/moveit/pull/3176/commits/f04a3a83294e993bc553bf9f962035b7cb383427
