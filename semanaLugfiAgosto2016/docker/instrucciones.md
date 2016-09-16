# Docker demo: Flask + postgre

El proposito de esta demo es mostrar como se conectan 2 contenedores, uno con un servidor flask (python), y otro con un servidor postgresql.

Las instrucciones asumen que ya está instalado y configurado el servicio docker de la máquina host.

## Levantando el servidor postgresql

Para levantar el servidor postgres, escribimos el siguiente comando:

	docker run --name postgres-server -e POSTGRES_PASSWORD=qwerty -d postgres

Desglosándolo:

* **docker run**: Crea un *contenedor* y lo ejecuta a partir de una imagen

* **--name postgres-server**: mi container se identificará como postgres-server

* **-e POSTGRES_PASSWORD=qwerty**: dentro del container habrá una variable de entorno *POSTGRES_PASSWORD* con el valor *qwerty*. Esta variable es utilizada por el contenedor para configurar la base de datos.

* **-d**: El contenedor se ejecuta en modo *detached*, es decir, como un proceso background del sistema.

* **postgres**: la imagen a partir de la cuál quiero crear mi container. La imagen postgresql está alojada en el registro público de docker, *hub.docker.io*. En caso de ser necesario, se descargará automáticamente.

La imagen postgres cuenta con el comando *EXPOSE 5432* dentro de su Dockerfile. Esto significa que fue compilada con la directiva de que su puerto 5432 pueda ser accedido desde cualquier ip.

## Compilando el servidor flask

### Dockerfile

El archivo *Dockerfile* es un archivo con una sintaxis bastante similar a bash, con las instrucciones para armar una *imagen* Docker.
A continuación se describen las lineas que lo componen:

* **FROM ubuntu**: La imagen está basada en una imagen ubuntu, para ser más preciso ubuntu:latest. Al igual que como se explicó en postgres, si la imagen no está presente, se descarga

* **RUN apt-get update..**: Se encadena una serie de comandos de bash (con el *&&* para que en caso de que falle una instrucción, falle toda la cadena). Se realiza todo en un mismo *run* para evitar la creación de capas innecesarias en la imagen, reduciendo el tamaño de la misma.

* **ADD server.py /opt/demo/**: Similar al comando *cp* de bash, copia el archivo server.py (ubicado junto al dockerfile) en el directorio /opt/demo

* **CMD python /opt/demo/server.py**: Comando default de mi imagen. Al iniciarse el container, se ejecuta un comando dividido en 2 parte: **Entrypoint** y **Cmd**.
El *entrypoint* es la primer parte del comando, suele ser */bin/bash*. Se puede sobreescribir con la opción --entrypoint.
El *cmd* es la segunda parte, generalmente el nombre de una aplicación que quiero ejecutar. Se sobreescribe agregando el comando deseado luego del nombre de la imagen a correr.

### Compilando

Para compilar la imagen con el servidor flask, correr el siguiente comando:

	docker build -t flask flask

Desglosándolo:

* **docker build**: crea una *imagen* a partir de un Dockerfile

* **-t flask**: la imagen se llamará *flask*

* **flask**: el Dockerfile se encuentra en la carpeta *flask*. La ruta puede ser relativa o absoluta. Si estamos posicionados en la misma carpeta que el dockerfile, se puede usar "."

## Levantando el servidor flask

Para levantar un container con el servidor demo, se utiliza el siguiente (gran) comando:

	docker run --name demo-server --link postgres-server:pg-server -p 5000:5000 flask 

Desglosando los nuevos atributos:

* **--link postgres-server:pg-server**: permite acceder desde el container *flask* a la interfaz de red del container *postgres-server*

* **-p5000:5000**: el puerto 5000 del container será bindeado al 5000 del host

## Preparando la db

Antes de correr la demo, se debe inicializar la base de datos. Si se utilizó la configuración propuesta, se puede correr un script sql con el siguiente comando:

psql -U postgres -h <host>

El usuario *postgres* viene precargado en la imagen descargada. *<host>* es la dirección del container con el servidor. El password que se pide por prompt es el que fue seteado como variable POSTGRES_PASSWORD

Ejecutar los comandos provistos en init_db.sql

### Conectando a postgre desde el host

Si tienen un cliente postgre en la máquina host, pueden conectarse a la ip del contenedor. La misma se puede averiguar haciendo

	docker inspect postgres-server | grep IPAddress

### Conectando a postgre desde otro container

Si no tienen un cliente psql en el host, y prefieren correrlo en un container para mantener más limpio el sistema, se pueden hacer los siguientes pasos:

	docker run --link postgres-server:pg-server -ti ubuntu
	apt-get install postgresql-client-9.x  (siendo *x* la versión disponible en el repositorio)

El primer paso inicia un container limpio basado en ubuntu, los flags *-t* e *i* indican que se habilite la entrada standard al contenedor, y que sea interactivo.
Este container iniciará una terminal bash, y el flag --link nos permite acceder al container postgres-server bajo el nombre pg-server. Se puede validar escribiendo *ping pg-server* (la ip debería ser la misma que la obtenida desde el host)

Si los containers fueron correctamente linkeados, se puede ejecutar

	psql -U postgres -h pg-server

**Tip**: Agregar el flag *-f <path_script>* en caso de que se quiera ejecutar un script sql en el servidor

## Comunicándose con flask

La comunicación con flask es por el puerto 5000. Al "bindear" este puerto al host, el puerto 5000 de nuestro host automáticamente nos redirige al puerto del container, por lo que podemos acceder mediante un browser a *http://localhost:5000/hello* para comprobar que funciona nuestro servicio de prueba "hello"

### Demo: consultando bd

Para consultar todos los usuarios disponibles, se debe realizar un GET al servicio */users*.

Con curl sería

	curl localhost:5000/users

Para agregar una entrada, se debe realizar un POST a la url con el formato */user/<username>*, con el nombre de la comida como data del post.

	curl localhost:5000/user/lingling -d "dog"

Para consultar las entradas de un solo usuario, el formato del servicio es igual que el post, solo que no envía datos.

	curl localhost:5000/user/lingling


## Tips

### Diferencia entre run y start

*docker run* implica la creación de un container nuevo, a partir de una imagen. Los containers tienen que tener distintos ids, por lo que debo tener cuidado al usar containers con nombre.
*docker start* implica reiniciar un container que estaba en estado stopped.

### Exportar containers

Se pueden exportar containers a un archivo .tar, estos pueden ser transportados e instalados con *docker import*.

Al importar un archivo se le puede dar un nombre para que genere una imagen a partir de él.

Tener en cuenta que generar una imagen desde un container, se pierde el Entrypoint y Cmd