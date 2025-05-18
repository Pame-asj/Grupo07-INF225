Para visualizar el servidor, es necesario tener **Django** instalado. Esto se puede hacer mediante el siguiente comando:

```bash
pip install django
```

La instalación puede llevarse a cabo dentro de un **entorno virtual** o directamente en el **sistema**, según se estime.

Luego, para iniciar el servidor, debe ubicarse en el directorio del proyecto (donde se encuentra el archivo `manage.py`) y si se trabaja en un entorno virtual linux ejecutar primero:

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install django #En este caso es necesario volver a instalar django
```
Y si no, basta con la siguiente linea:

```bash
python manage.py runserver
```

Podrá acceder al prototipo a través de navegador web, ingresando a la siguiente dirección:

```
http://127.0.0.1:8000
```
*Aclarar que en un inicio tanemos un sistema de login manual que posteriormente sera cambiado, ahora solo esta así para probar el prototipo inicial*
