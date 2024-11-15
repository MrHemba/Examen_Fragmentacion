import psycopg
import pyodbc

# Conexión a PostgreSQL
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
    except Exception as e:
        print("Error al conectar a SQL Server:", e)
        return None

# Recuperar datos de SQL Server
def recuperar_datos_sql_server():
    conexion_sql = conectar_sql_server()

    if conexion_sql:
        try:
            cursor_sql = conexion_sql.cursor()
            cursor_sql.execute("SELECT * FROM company")  
            registros_sql = cursor_sql.fetchall()
            cursor_sql.close()
            return registros_sql
        except Exception as e:
            print("Error al recuperar datos de SQL Server:", e)
            return []

# Recuperar datos de PostgreSQL
def recuperar_datos_postgresql():
    conexion_pg = conectar_postgresql()

    if conexion_pg:
        try:
            cursor_pg = conexion_pg.cursor()
            cursor_pg.execute("SELECT * FROM employee")  
            registros_pg = cursor_pg.fetchall()
            cursor_pg.close()
            return registros_pg
        except Exception as e:
            print("Error al recuperar datos de PostgreSQL:", e)
            return []

# Unificar y ordenar por ID
def unificar_datos():
   
    registros_sql = recuperar_datos_sql_server()
    registros_pg = recuperar_datos_postgresql()

    registros_unificados = registros_sql + registros_pg
    registros_unificados_ordenados = sorted(registros_unificados, key=lambda x: x[0])
    for registro in registros_unificados_ordenados:
        print(registro)

unificar_datos()
