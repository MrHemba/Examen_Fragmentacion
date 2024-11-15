import psycopg

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

def recuperar_datos_postgresql():
    conexion_pg = conectar_postgresql()

    if conexion_pg:
        try:
            cursor_pg = conexion_pg.cursor()

            cursor_pg.execute("SELECT * FROM employee")  
            registros = cursor_pg.fetchall()  

           
            for registro in registros:
                print(registro) 

            cursor_pg.close()  
        except Exception as e:
            print("Error al recuperar datos de PostgreSQL:", e)
        finally:
            conexion_pg.close()  

recuperar_datos_postgresql()
