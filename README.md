# 🛡️Inyección SQL (SQLi) con Docker

Un entorno de pruebas interactivo y aislado para comprender, explotar y mitigar vulnerabilidades de Inyección SQL en aplicaciones web. Este proyecto demuestra visualmente la diferencia entre construir consultas de base de datos de forma insegura (concatenación) y de forma segura (consultas parametrizadas).

## 🚀 Tecnologías Utilizadas

* **Backend:** Python 3.9, Flask
* **Base de Datos:** PostgreSQL 17
* **Infraestructura:** Docker, Docker Compose
* **Frontend:** HTML5, Bootstrap 5

## 🎯 Objetivo del Proyecto

El propósito de esta prueba educativo. Permite observar en tiempo real cómo el motor de la base de datos interpreta las entradas del usuario. Cuenta con dos rutas principales:
1.  **Ruta Vulnerable (`/vulnerable`):** Susceptible a ataques lógicos, inyecciones UNION y consultas apiladas (Stacked Queries).
2.  **Ruta Segura (`/seguro`):** Protegida mediante el uso estricto de consultas preparadas/parametrizadas, bloqueando cualquier intento de inyección.

## ⚙️ Instalación y Ejecución

Al estar completamente dockerizado, levantar el proyecto es rápido y no ensucia tu sistema local.

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/warinsanomachine/proyecto_sqli]([https://github.com/tu-usuario/laboratorio-sqli.git](https://github.com/warinsanomachine/proyecto_sqli))
    cd proyecto_sqli
    ```

2.  **Construye y levanta los contenedores:**
    ```
    docker-compose up --build
    ```

3.  **Accede a la aplicación:**
    Abre tu navegador web y dirígete a `http://localhost:5000`.

*(Nota: Si necesitas reiniciar la base de datos para recuperar los registros originales, ejecuta `docker-compose down -v` seguido de `docker-compose up --build`).*

## 🧪 Pruebas de Concepto (Payloads)

Una vez en la aplicación web, puedes utilizar el formulario del lado "Vulnerable" para probar las siguientes técnicas:

* **Bypass de Autenticación (Extracción de todos los datos):**
    ```sql
    ' OR '1'='1
    ```
* **Escalada de Privilegios Dirigida (Filtrar por rol):**
    ```sql
    ' OR rol = 'Administrador' --
    ```
* **Inyección Destructiva (Consultas Apiladas - Cambiar contraseñas):**
    ```sql
    '; UPDATE usuarios SET clave_secreta = 'hackeado'; --
    ```

Prueba estos mismos *payloads* en el formulario "Seguro" para comprobar cómo las consultas parametrizadas neutralizan el ataque al interpretar el texto de forma literal.

## 📁 Estructura del Proyecto

```text
/
├── app.py                # Lógica del servidor web (Flask) y conexión a BD
├── docker-compose.yml    #
├── Dockerfile            # Construcción de la imagen de Python
├── init.sql              # Script de inicialización de tablas y registros
└── requirements.txt      # Dependencias de Python (Flask, psycopg2)
