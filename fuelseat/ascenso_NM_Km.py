def tiempo_para_ascenso(altitud, regimen):
    return altitud / regimen

def convertir_a_minutos_segundos(tiempo_total):
    minutos = int(tiempo_total)
    segundos = (tiempo_total - minutos) * 60
    return minutos, segundos

def kts_a_nm_por_minuto(velocidad_kts):
    return velocidad_kts / 60

def nm_a_km(distancia_nm):
    return distancia_nm * 1.852

def main():
    while True:
        print("\nCalculadora de tiempo de ascenso para una aeronave")
        print("1. Calcular tiempo de ascenso y distancia recorrida en km")
        print("2. Salir")
        opcion = input("Seleccione una opción (1, 2): ")

        if opcion == '1':
            try:
                altitud = float(input("Ingrese la altitud a alcanzar en pies (ft): "))
                regimen = float(input("Ingrese el régimen de ascenso en pies por minuto (ft/min): "))
                velocidad_kts = float(input("Ingrese la velocidad en nudos (kts): "))
                
                if altitud <= 0 or regimen <= 0 or velocidad_kts <= 0:
                    print("Los valores ingresados deben ser mayores que cero. Inténtelo de nuevo.")
                else:
                    tiempo_total = tiempo_para_ascenso(altitud, regimen)
                    minutos, segundos = convertir_a_minutos_segundos(tiempo_total)
                    nm_por_minuto = kts_a_nm_por_minuto(velocidad_kts)
                    distancia_nm = nm_por_minuto * tiempo_total
                    distancia_km = nm_a_km(distancia_nm)
                    
                    print(f"El tiempo necesario para alcanzar {altitud} ft con un régimen de ascenso de {regimen} ft/min y una velocidad de {velocidad_kts} kts es aproximadamente {minutos} minutos y {segundos:.2f} segundos.")
                    print(f"En ese tiempo, la aeronave recorre aproximadamente {distancia_km:.2f} kilómetros.")
                    
            except ValueError:
                print("Por favor, ingrese valores numéricos válidos.")

        elif opcion == '2':
            print("Saliendo de la calculadora. ¡Adiós!")
            break

        else:
            print("Opción no válida, por favor intente nuevamente.")

if __name__ == "__main__":
    main()
