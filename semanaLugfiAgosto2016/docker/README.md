# README

El propósito de la demo es mostrar cómo se puede testear una aplicación web en un contenedor, y que se comunique con una fuente de datos en otro contenedor

## ¿Por qué docker?

A diferencia de las Virtual machines, los contenedores son mucho más livianos debido a que no emulan hardware, sino que crean entornos virtuales para las aplicaciones. Esto hace que crear y ejecutar un contenedor sea mucho más ágil y volátil.

El sistema de archivos de docker está basado en *layers*, una imagen base puede estar formada por una o varias capas de escritura, y crear un contenedor implica crear una capa (layer) encima de la imagen. Estas capas son fáciles de crear y eliminar, y permitir que la imagen permanezca intacta, facilita enormemente la clonación de entornos vírgenes de trabajo.

## ¿Containers? ¿Imágenes?

Como se dijo antes, un container es como un entorno virtual. Una imagen es un "Template" de lo que serán los contenedores. Por ejemplo, ubuntu es una imagen que contiene algunas de las aplicaciones básicas para simular un ambiente de trabajo Ubuntu. Si yo quiero trabajar sobre un ubuntu virgen, ejecuto *docker run -ti ubuntu* y se genera un container con la base Ubuntu. Todas las modificaciones que haga serán sobre el container.
Cuando cierre la terminal, el container pasará a un estado stopped, con los cambios almacenados, **hasta que sea borrado de la cache**
Si quiero un nuevo ubuntu virgen, puedo volver a correr *docker run*, pero debo tener en cuenta que esto genera otro container nuevo más, por lo que periódicamente tengo que liberar espacio


## ¿Qué se almacena? ¿Que se borra?

Los cambios almacenados en un container quedan *en esa instancia del container*. Si quiero persistir los cambios realizados en un container, hay 2 formas:

* Crear una imagen a partir de un container

* Utilizar volúmenes montados

La primera opción consiste en realizar un commit

La segunda opción consiste en, mediante el flag -v, permitir al contenedor montar un directorio del host como si fuera propio. De esta manera, cuando modifico el directorio montado, los cambios se persisten en el host.

Ejemplo: docker run -v /home/barba/docker-logs:/opt/server/logs

Si en mi container escribo en la carpeta /opt/server/logs (creo o modifico un archivo), el cambio se ve reflejado en el home de mi host. Notar que los permisos del host se mantienen en el container y viceversa, por lo que, crear un archivo con root desde el container implica que este será de root en el host.

## Pero... ¿Por qué?

Para asegurarse que los datos utilizados en los tests siempre están limpios, es una buena idea realizar los tests sobre containers de docker y luego desecharlos. Docker nos permite tener entornos de desarrollo limpios, ahorrándonos problemas como "en mi máquina compila", "olvidé de tirar la base de datos", "tengo tantas bibliotecas instaladas que no se cuáles son las necesarias para correr mi aplicación"