import sqlite3
import sys
import os


from Fuel_seat import conectar_base_datos_rutas
from Fuel_seat import verificar_y_crear_tabla_rutas_aereas
from Fuel_seat import obtener_distancia_vuelo
from Fuel_seat import obtener_datos_usuario
from Fuel_seat import obtener_datos_consumo_combustible
from Fuel_seat import calcular_tiempo_vuelo
from Fuel_seat import calcular_consumo_total
from Fuel_seat import calcular_costo_combustible
from Fuel_seat import calcular_consumo_por_pasajero



module_path = os.path.abspath(os.path.join(".."))

if module_path not in sys.path:
    sys.path.append(module_path)

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