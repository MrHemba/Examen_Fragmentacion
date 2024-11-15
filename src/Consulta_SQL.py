import pyodbc

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

def recuperar_datos_sql_server():
    conexion_sql = conectar_sql_server()

    if conexion_sql:
        try:
            cursor_sql = conexion_sql.cursor()
      
            cursor_sql.execute("SELECT * FROM company") 
            registros = cursor_sql.fetchall() 

            for registro in registros:
                print(registro)  

            cursor_sql.close()  

        except Exception as e:
            print("Error al recuperar datos de SQL Server:", e)
        finally:
            conexion_sql.close() 

recuperar_datos_sql_server()
