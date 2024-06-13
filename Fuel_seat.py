import sqlite3

# Función para conectar a la base de datos de rutas aéreas
def conectar_base_datos_rutas():
    try:
        conexion = sqlite3.connect(r"E:\repogit\pydev_projects\RutasAereasCOR.db")
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

# Función principal del programa
def main():
    try:
        # Obtener datos del usuario y seleccionar la aeronave
        aeronave, pasajeros, origen, destino, velocidad_viento, altitud_crucero = obtener_datos_usuario()
        
        if aeronave is None:
            return
        
        # Convertir origen y destino a mayúsculas
        origen = origen.upper()
        destino = destino.upper()
        
        # Obtener distancia de vuelo desde la base de datos
        distancia_km = obtener_distancia_vuelo(origen, destino)
        
        if distancia_km is None:
            return
        
        # Obtener consumo de combustible (ejemplo)
        consumo_combustible = 4.5 if aeronave == "B738" else 3.8
        
        # Velocidad de crucero fija para ambas aeronaves (ejemplo)
        velocidad_crucero = 490  # nudos (kts)
        
        # Calcular tiempo de vuelo en horas
        tiempo_vuelo = calcular_tiempo_vuelo(distancia_km, velocidad_crucero)
  
        # Calcular consumo total de combustible en litros
        consumo_total = calcular_consumo_total(distancia_km, consumo_combustible)
        
        # Calcular costo total de combustible (suponiendo precio por litro)
        precio_combustible_por_litro = 1.5  # Ejemplo de precio por litro
        costo_combustible_total = calcular_costo_combustible(consumo_total, precio_combustible_por_litro)
        
        # Calcular consumo por pasajero en litros
        consumo_por_pasajero = calcular_consumo_por_pasajero(consumo_total, pasajeros)
        
        # Calcular asientos no ocupados (ejemplo)
        asientos_maximos = 170 if aeronave == "B738" else 96
        asientos_no_ocupados = asientos_maximos - pasajeros
        
        # Calcular costo por asientos no ocupados en USD (ejemplo)
        costo_asientos_no_ocupados = asientos_no_ocupados * consumo_combustible * precio_combustible_por_litro
        
        # Sumar el costo por asientos no ocupados al costo total de combustible
        costo_combustible_total += costo_asientos_no_ocupados
        
        # Asumiendo una ganancia fija por cada asiento ocupado (ejemplo)
        ganancia_por_asiento_ocupado = 50  # Ejemplo de ganancia por asiento ocupado en USD
        ganancia_total_asientos_ocupados = pasajeros * ganancia_por_asiento_ocupado
        
        # Mostrar resultados con unidades y redondeados a dos decimales
        
        print(f"Tiempo de vuelo estimado: {tiempo_vuelo:.2f} horas")
        print(f"Consumo total de combustible: {int(consumo_total)} litros")
        print(f"Costo total de combustible: ${costo_combustible_total:.2f} USD")
        print(f"Consumo por pasajero: {int(consumo_por_pasajero)} litros/seat")
        print(f"Costo por asientos no ocupados: ${float(costo_asientos_no_ocupados)} USD")
        print(f"Ganancia total por asientos ocupados: ${int(ganancia_total_asientos_ocupados)} USD")

        # Esperar la entrada del usuario para salir
        input("Presiona Enter para salir...")
    
    except ValueError as e:
        print(f"Error: {e}")
        
    except Exception as e:
        print(f"Error en el programa: {e}")

# Llamar a la función principal para ejecutar el programa
if __name__ == "__main__":
    main()

                #//////////////////////////////////////////////////////////////////////////////////#
# Pendiente de agregar al programa que el usuario al agregar el valor del viento en kts afecte al tiempo de recorrido de la aeronave
# No está funcionando la lectura de la base de datos porque al ingresar el usuario el techo o nivel de vuelo eso tambien afecta al tiempo de recorrido de dicha aeronave
                #//////////////////////////////////////////////////////////////////////////////////#
                                # DADO POR FINALIZADO HASTA LA CORRECION #