from flask import Flask
from flask_restx import Api, Resource, fields
import psycopg  
import pyodbc  

# Inicializar la aplicación Flask
app = Flask(__name__)

# Crear una instancia de la API Flask-RESTX
api = Api(app, doc='/swagger/')  # '/swagger/' es la ruta para la documentación Swagger

# Definir el modelo de datos para el empleado
employee_model = api.model('Employee', {
    'employeeId': fields.Integer(required=True, description='The employee identifier'),
    'name': fields.String(required=True, description='The name of the employee'),
    'department': fields.String(required=True, description='The department of the employee'),
    'location': fields.String(required=True, description='The location of the employee')
})

def conectar_postgresql():
    try:
        conexion_pg = psycopg.connect(
            host='localhost',
            dbname='company', 
            user='postgres',   
            password='julio2002',  
            port='5432'
        )
        return conexion_pg
    except Exception as ex:
        print("Error al conectar a PostgreSQL:", ex)
        return None


def conectar_sql_server():
    try:
        conexion_sql = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"  
            "DATABASE=company;" 
            "UID=anthony;" 
            "PWD=julio2002;"  
        )
        print("Conexión a SQL Server exitosa")
        return conexion_sql
    except Exception as e:
        print("Error al conectar a SQL Server:", e)
        return None

def consultar_postgresql(employeeid):
    conexion_pg = conectar_postgresql()
    if not conexion_pg:
        return None

    try:
        cursor = conexion_pg.cursor()
        cursor.execute("SELECT * FROM employee WHERE EmployeeID = %s", (employeeid,))
        resultado = cursor.fetchone()
        if resultado:
            return {
                'employeeId': resultado[0],
                'name': resultado[1],
                'department': resultado[2],
                'location': resultado[3]
            }
    except Exception as e:
        print("Error en la consulta a PostgreSQL:", e)
    finally:
        conexion_pg.close()
    return None

def consultar_sql_server(employeeid):
    conexion_sql = conectar_sql_server()
    if not conexion_sql:
        return None

    try:
        cursor = conexion_sql.cursor()
        cursor.execute("SELECT * FROM company WHERE EmployeID = ?", (employeeid,))
        resultado = cursor.fetchone()
        if resultado:
            return {
                'employeeId': resultado[0],
                'name': resultado[1],
                'department': resultado[2],
                'location': resultado[3]
            }
    except Exception as e:
        print("Error en la consulta a SQL Server:", e)
    finally:
        conexion_sql.close()
    return None

# Clase Resource para manejar las solicitudes GET
class Employee(Resource):
    @api.marshal_with(employee_model)
    def get(self, employeeid):
        """
        Obtener la información de un empleado por su ID.
        Primero consulta en PostgreSQL. Si no encuentra resultados, consulta en SQL Server.
        """
        # Consultar en PostgreSQL
        employee_data = consultar_postgresql(employeeid)
        if employee_data:
            return employee_data

        # Si no se encuentra en PostgreSQL, consultar en SQL Server
        employee_data = consultar_sql_server(employeeid)
        if employee_data:
            return employee_data

        # Si no se encuentra en ninguna base de datos
        return {'message': 'Empleado no encontrado'}, 404

api.add_resource(Employee, '/employees/<int:employeeid>')

if __name__ == '__main__':
    app.run(debug=True)
