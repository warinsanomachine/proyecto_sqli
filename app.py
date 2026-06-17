from flask import Flask, request, render_template_string
import psycopg2

aplicacion = Flask(__name__)

def obtener_conexion():
    conexion = psycopg2.connect(
        dbname="base_datos_sqli",
        user="usuario_db",
        password="clave_db",
        host="db"
    )
    conexion.autocommit = True
    return conexion

plantilla_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Laboratorio SQLi</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h2 class="text-center mb-4">Laboratorio de Inyección SQL</h2>
        <div class="row">
            <div class="col-md-6">
                <div class="card shadow-sm border-danger">
                    <div class="card-header bg-danger text-white">
                        Prueba Vulnerable (Concatenación)
                    </div>
                    <div class="card-body">
                        <form method="POST" action="/vulnerable">
                            <div class="mb-3">
                                <label class="form-label">Usuario:</label>
                                <input type="text" class="form-control" name="nombre_usuario" required>
                            </div>
                            <button type="submit" class="btn btn-danger w-100">Buscar (Vulnerable)</button>
                        </form>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card shadow-sm border-success">
                    <div class="card-header bg-success text-white">
                        Prueba Segura (Parámetros)
                    </div>
                    <div class="card-body">
                        <form method="POST" action="/seguro">
                            <div class="mb-3">
                                <label class="form-label">Usuario:</label>
                                <input type="text" class="form-control" name="nombre_usuario" required>
                            </div>
                            <button type="submit" class="btn btn-success w-100">Buscar (Seguro)</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        {% if consulta_ejecutada %}
        <div class="alert alert-warning mt-4 font-monospace">
            <strong>Consulta Ejecutada:</strong> <br> {{ consulta_ejecutada }}
        </div>
        {% endif %}

        {% if resultados is not none %}
        <div class="card mt-4 shadow-sm">
            <div class="card-header bg-dark text-white">Resultados de la Base de Datos</div>
            <div class="card-body">
                {% if resultados|length > 0 %}
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Usuario</th>
                                <th>Contraseña</th>
                                <th>Rol</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for fila in resultados %}
                            <tr>
                                <td>{{ fila[0] }}</td>
                                <td>{{ fila[1] }}</td>
                                <td>{{ fila[2] }}</td>
                                <td><span class="badge bg-primary">{{ fila[3] }}</span></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                {% else %}
                    <p class="text-muted mb-0">No se encontraron resultados.</p>
                {% endif %}
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@aplicacion.route('/')
def inicio():
    return render_template_string(plantilla_html, resultados=None, consulta_ejecutada=None)

@aplicacion.route('/vulnerable', methods=['POST'])
def ruta_vulnerable():
    nombre_usuario = request.form['nombre_usuario']
    conexion = obtener_conexion()
    cursor_bd = conexion.cursor()
    
    consulta_sql = f"SELECT * FROM usuarios WHERE nombre_usuario = '{nombre_usuario}';"
    
    try:
        cursor_bd.execute(consulta_sql)
        if cursor_bd.description:
            resultados_bd = cursor_bd.fetchall()
        else:
            resultados_bd = [("Comando ejecutado. Base de datos modificada.", "", "", "")]
    except Exception as error_bd:
        resultados_bd = [(str(error_bd), "", "", "")]
        
    cursor_bd.close()
    conexion.close()
    return render_template_string(plantilla_html, resultados=resultados_bd, consulta_ejecutada=consulta_sql)

@aplicacion.route('/seguro', methods=['POST'])
def ruta_segura():
    nombre_usuario = request.form['nombre_usuario']
    conexion = obtener_conexion()
    cursor_bd = conexion.cursor()
    
    consulta_sql = "SELECT * FROM usuarios WHERE nombre_usuario = %s;"
    consulta_visual = f"SELECT * FROM usuarios WHERE nombre_usuario = '{nombre_usuario}'; (Protegido)"
    
    try:
        cursor_bd.execute(consulta_sql, (nombre_usuario,))
        if cursor_bd.description:
            resultados_bd = cursor_bd.fetchall()
        else:
            resultados_bd = [("Comando ejecutado. Base de datos modificada.", "", "", "")]
    except Exception as error_bd:
        resultados_bd = [(str(error_bd), "", "", "")]
        
    cursor_bd.close()
    conexion.close()
    return render_template_string(plantilla_html, resultados=resultados_bd, consulta_ejecutada=consulta_visual)

if __name__ == '__main__':
    aplicacion.run(host='0.0.0.0', port=5000)