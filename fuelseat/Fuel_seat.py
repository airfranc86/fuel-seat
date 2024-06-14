import sqlite3

# Función para conectar a la base de datos de rutas aéreas
def conectar_base_datos_rutas():
    try:
        #conexion = sqlite3.connect(r"E:\repogit\pydev_projects\RutasAereasCOR.db")
        conexion = sqlite3.connect(r"../RutasAereasCOR.db")
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

# Función para obtener la distancia de vuelo desde la base de datos de rutas aéreas
def obtener_distancia_vuelo(origen, destino):
    try:
        conexion = conectar_base_datos_rutas()
        if conexion is None:
            return None
        
        cursor = conexion.cursor()
        cursor.execute("SELECT distancia_km FROM RutasAereas WHERE origen = ? AND destino = ?", (origen, destino))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado:
            return resultado[0]
        else:
            print("Ruta no encontrada en la base de datos.")
            return None
    
    except Exception as e:
        print(f"Error al obtener distancia de vuelo: {e}")
        return None

# Función para obtener los datos del usuario
def obtener_datos_usuario():
    try:
        opcion = int(input("Seleccione la aeronave:\n1. Boeing 737-800 (B738)\n2. Embraer 190 (E190)\nOpción: "))
        if opcion == 1:
            aeronave = "B738"
        elif opcion == 2:
            aeronave = "E190"
        else:
            raise ValueError("Opción inválida")
        
        pasajeros = int(input("Ingrese la cantidad de pasajeros a bordo: "))
        origen = input("Ingrese el código IATA del aeropuerto de origen (e.g., COR): ").strip().upper()
        destino = input("Ingrese el código IATA del aeropuerto de destino (e.g., AEP): ").strip().upper()
        velocidad_viento = float(input("Ingrese la velocidad del viento en nudos (kts): "))
        altitud_crucero = int(input("Ingrese la altitud de crucero (FL): "))
        
        return aeronave, pasajeros, origen, destino, velocidad_viento, altitud_crucero
    
    except ValueError as e:
        print(f"Error: {e}")
        return None, None, None, None, None, None

# Función para obtener los datos de consumo de combustible según la aeronave y fase del vuelo
def obtener_datos_consumo_combustible(aeronave, fase_vuelo):
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()
        
        # Escoger la tabla adecuada según la aeronave
        tabla_consumo = f"Consumo_Fuel{aeronave}"
        
        # Consultar los valores de consumo para la fase de vuelo especificada
        cursor.execute(f"SELECT {fase_vuelo} FROM {tabla_consumo}")
        resultado = cursor.fetchone()
        
        conexion.close()
        
        if resultado:
            return resultado[0]
        else:
            print(f"No se encontraron datos para {aeronave} en la fase de vuelo {fase_vuelo}.")
            return None
        
    except Exception as e:
        print(f"Error al obtener datos de consumo de combustible: {e}")
        return None


# Función para calcular el tiempo de vuelo en horas
def calcular_tiempo_vuelo(distancia_km, velocidad_crucero):
    tiempo_horas = distancia_km / velocidad_crucero
    return tiempo_horas

# Función para calcular el consumo total de combustible en litros
def calcular_consumo_total(distancia_km, consumo_combustible):
    consumo_total = consumo_combustible * distancia_km
    return consumo_total

# Función para calcular el costo total del combustible
def calcular_costo_combustible(consumo_total, precio_combustible_por_litro):
    costo_total = consumo_total * precio_combustible_por_litro
    return costo_total

# Función para calcular el consumo por pasajero en litros
def calcular_consumo_por_pasajero(consumo_total, pasajeros):
    consumo_por_pasajero = consumo_total / pasajeros
    return consumo_por_pasajero