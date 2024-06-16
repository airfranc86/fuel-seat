import sqlite3
import os

# Función para conectar a la base de datos de rutas aéreas
def conectar_base_datos_rutas():
    try:
        # Ubicación de este archivo
        directorio_script = os.path.dirname(os.path.abspath(__file__))

        # Ruta relativa hacia la base de datos
        ruta_base_datos = os.path.join(directorio_script, "datos/RutasAereasCOR.db")

        # Conexión a la base de datos
        conexion = sqlite3.connect(ruta_base_datos)

        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos de rutas aéreas: {e}")
        return None



# Función para verificar y crear la tabla RutasAereas si no existe
def verificar_y_crear_tabla_rutas_aereas(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='RutasAereas';")
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            cursor.execute('''CREATE TABLE RutasAereas (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                origen TEXT NOT NULL,
                                destino TEXT NOT NULL,
                                distancia_km REAL NOT NULL
                              );''')
            cursor.execute("INSERT INTO RutasAereas (origen, destino, distancia_km) VALUES ('COR', 'AEP', 710)")
            cursor.execute("INSERT INTO RutasAereas (origen, destino, distancia_km) VALUES ('AEP', 'COR', 710)")
            conexion.commit()
    
    except Exception as e:
        print(f"Error al verificar o crear la tabla RutasAereas: {e}")


