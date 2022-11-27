cp comandos/*.sh ../../
chmod +x ../../*.sh
chmod +x project_pkg/scripts/*.py
unzip class_pkgs/yolo.zip -d class_pkgs/
cd ../../
catkin_make
echo "El proyecto a sido configurado"