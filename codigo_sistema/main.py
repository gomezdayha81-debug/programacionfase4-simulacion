from modelos import Cliente
from gestion import ReservaSala, AlquilerEquipos, AsesoriaEspecializada, Reserva
from excepciones import ErrorSoftwareFJ, registrar_log

def ejecutar_simulador():
    print("=== INICIANDO SIMULACIÓN DE OPERACIONES SOFTWARE FJ ===")
    registrar_log("SISTEMA", "Inicio del simulador principal de pruebas.")
    
    # Contenedores en memoria (sin bases de datos)
    clientes_validos = []
    servicios_validos = []
    
    # -------------------------------------------------------------
    # OPERACIONES 1-3: Intentos de Registro de Clientes
    # -------------------------------------------------------------
    print("\n--- Evaluando Registro de Clientes ---")
    # Caso 1: Cliente Válido
    try:
        c1 = Cliente("C001", "Carlos Pérez", "carlos@email.com")
        clientes_validos.append(c1)
        print("[OK] Cliente 1 registrado.")
    except ErrorSoftwareFJ as e:
        print(f"[CONTROLADO] Error en Caso 1: {e}")

    # Caso 2: Cliente con Correo Inválido (Falla)
    try:
        c2 = Cliente("C002", "Ana Gómez", "anagomez.com")
    except ErrorSoftwareFJ as e:
        print(f"[CONTROLADO] Error en Caso 2 (Esperado): {e}")

    # Caso 3: Cliente Válido
    try:
        c3 = Cliente("C003", "Marta Soler", "marta@email.com")
        clientes_validos.append(c3)
        print("[OK] Cliente 3 registrado.")
    except ErrorSoftwareFJ as e:
        print(f"[CONTROLADO] Error en Caso 3: {e}")

    # -------------------------------------------------------------
    # OPERACIONES 4-6: Creación de Servicios
    # -------------------------------------------------------------
    print("\n--- Evaluando Creación de Servicios ---")
    # Caso 4: Sala Válida
    try:
        s1 = ReservaSala("S_SALA_01", 50000, capacidad_personas=12)
        servicios_validos.append(s1)
        print("[OK] Servicio Sala registrado.")
    except ErrorSoftwareFJ as e:
        print(f"[CONTROLADO] Error en Caso 4: {e}")

    # Caso 5: Sala Inválida (Capacidad cero -> Falla)
    try:
        s2 = ReservaSala("S_SALA_02", 40000, capacidad_personas=0)
    except ErrorSoftwareFJ as e:
        print(f"[CONTROLADO] Error en Caso 5 (Esperado): {e}")

    # Caso 6: Alquiler de Equipo Válido
    try:
        s3 = AlquilerEquipos("S_EQ_01", 25000, requiere_seguro=True)
        servicios_validos.append(s3)
        print("[OK] Servicio Equipos registrado.")
    except ErrorSoftwareFJ as e:
        print(f"[CONTROLADO] Error en Caso 6: {e}")

    # -------------------------------------------------------------
    # OPERACIONES 7-10: Gestión de Reservas y Cálculos
    # -------------------------------------------------------------
    print("\n--- Evaluando Reservas y Procesamientos ---")
    
    # Caso 7: Reserva Exitosa (Sala por 4 horas con descuento)
    try:
        if clientes_validos and servicios_validos:
            reserva1 = Reserva("R001", clientes_validos[0], servicios_validos[0], duracion=4)
            reserva1.procesar_confirmacion(descuento=15000)
    except ErrorSoftwareFJ as e:
        print(f"[CONTROLADO] Error en Caso 7: {e}")

    # Caso 8: Reserva Fallida por duración inválida (-2 horas)
    try:
        reserva2 = Reserva("R002", clientes_validos[0], servicios_validos[0], duracion=-2)
        reserva2.procesar_confirmacion()
    except ErrorSoftwareFJ as e:
        print(f"[CONTROLADO] Error en Caso 8 (Esperado): {e}")

    # Caso 9: Reserva Exitosa (Equipo por 3 días)
    try:
        if len(clientes_validos) > 1 and len(servicios_validos) > 1:
            reserva3 = Reserva("R003", clientes_validos[1], servicios_validos[1], duracion=3)
            reserva3.procesar_confirmacion(impuesto=0.19)
    except ErrorSoftwareFJ as e:
        print(f"[CONTROLADO] Error en Caso 9: {e}")

    # Caso 10: Reserva con Error de encadenamiento (Parámetro erróneo enviado al cálculo)
    try:
        if clientes_validos and servicios_validos:
            reserva4 = Reserva("R004", clientes_validos[0], servicios_validos[0], duracion=5)
            # Pasamos un tipo incorrecto en el descuento para forzar error en el cálculo interno
            reserva4.procesar_confirmacion(descuento="TextoInvalido")
    except ErrorSoftwareFJ as e:
        print(f"[CONTROLADO] Error en Caso 10 (Esperado/Encadenado): {e}")

    print("\n=== SIMULACIÓN FINALIZADA SIN CAÍDAS DEL SISTEMA ===")
    registrar_log("SISTEMA", "Simulación finalizada exitosamente.")

if __name__ == "__main__":
  if __name__ == "__main__":
    import os
    ejecutar_simulador()
    print("\n[RUTA] El archivo errores.log se guardó en:")
    print(os.path.abspath("errores.log"))
    input("\nPresiona Enter para cerrar...")
