import psycopg
import pyodbc

# Conexión a PostgreSQL
def conectar_postgresql():
    try:
        conexion_pg = psycopg.connect(
            host='localhost',
            dbname='company',  # Agrega el nombre de tu base de datos
            user='postgres',
            password='julio2002',
            port='5432'
        )
        print("Conexión a PostgreSQL exitosa")
        return conexion_pg
    except Exception as ex:
        print("Error al conectar a PostgreSQL:", ex)
        return None

# Conexión a SQL Server
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
    except Exception as ex:
        print("Error al conectar a SQL Server:", ex)
        return None

# Fragmentación y transferencia de datos
def fragmentar_y_transferir():
    conexion_pg = conectar_postgresql()
    conexion_sql = conectar_sql_server()

    if conexion_pg and conexion_sql:
        try:
            # Fragmentación: Seleccionar datos para SQL Server (San Francisco)
            cursor_pg = conexion_pg.cursor()
            cursor_pg.execute("SELECT * FROM employee WHERE Location = 'San Francisco'")
            registros_san_francisco = cursor_pg.fetchall()

            # Insertar datos fragmentados en SQL Server
            cursor_sql = conexion_sql.cursor()
            for registro in registros_san_francisco:
                consulta_sql = """
                INSERT INTO company (EmployeID, Name, Department, Location)
                VALUES (?, ?, ?, ?)
                """
                cursor_sql.execute(consulta_sql, registro)
            conexion_sql.commit()

            print("Datos con Location = 'San Francisco' transferidos a SQL Server")

            # Eliminar registros transferidos de PostgreSQL
            cursor_pg.execute("DELETE FROM employee WHERE Location = 'San Francisco'")
            conexion_pg.commit()

            print("Datos con Location = 'San Francisco' eliminados de PostgreSQL")

        except Exception as e:
            print("Error durante la transferencia de datos:", e)
        finally:
            cursor_pg.close()
            cursor_sql.close()
            conexion_pg.close()
            conexion_sql.close()
    else:
        print("No se pudo establecer la conexión con una o ambas bases de datos.")

# Ejecutar la fragmentación y transferencia
fragmentar_y_transferir()
