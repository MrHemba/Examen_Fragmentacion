from xmlrpc.server import SimpleXMLRPCServer
import psycopg
import pyodbc

# Función para conectarse a PostgreSQL
def conectar_postgresql():
    try:
        conexion_pg = psycopg.connect(
            host="localhost",
            dbname="company",
            user="postgres",
            password="julio2002",
            port=5432
        )
        print("Conexión a PostgreSQL exitosa")
        return conexion_pg
    except Exception as e:
        print("Error al conectar a PostgreSQL:", e)
        return None

# Función para conectarse a SQL Server
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

# Función RPC para obtener datos del empleado
def getEmployeeData(employeeID):
    try:
        # Conexión a PostgreSQL
        conexion_pg = conectar_postgresql()
        if conexion_pg:
            cursor_pg = conexion_pg.cursor()
            cursor_pg.execute("SELECT * FROM employee WHERE employeeid = %s", (employeeID,))
            resultado_pg = cursor_pg.fetchone()
            if resultado_pg:
                cursor_pg.close()
                conexion_pg.close()
                return list(resultado_pg)  # Convertir a lista serializable

        # Conexión a SQL Server
        conexion_sql = conectar_sql_server()
        if conexion_sql:
            cursor_sql = conexion_sql.cursor()
            cursor_sql.execute("SELECT * FROM company WHERE EmployeID = ?", (employeeID,))
            resultado_sql = cursor_sql.fetchone()
            if resultado_sql:
                cursor_sql.close()
                conexion_sql.close()
                return list(resultado_sql)  # Convertir a lista serializable

        return "Empleado no encontrado en ninguna base de datos"
    except Exception as e:
        return f"Error al buscar el empleado: {e}"

# Iniciar servidor RPC
server = SimpleXMLRPCServer(("localhost", 8000))
print("Servidor RPC corriendo en el puerto 8000...")

# Registrar la función RPC
server.register_function(getEmployeeData, "getEmployeeData")

# Ejecutar el servidor
server.serve_forever()
