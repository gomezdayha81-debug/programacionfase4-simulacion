from modelos import Servicio, Cliente
from excepciones import ServicioNoDisponibleError, ReservaInvalidaError, registrar_log

# --- Servicios Especializados ---

class ReservaSala(Servicio):
    def __init__(self, id_servicio, precio_base, capacidad_personas: int):
        super().__init__(id_servicio, "Reserva de Sala", precio_base)
        self.capacidad_personas = capacidad_personas
        self.validar_parametros()

    def validar_parametros(self):
        if self.capacidad_personas <= 0:
            raise ServicioNoDisponibleError("La capacidad de la sala debe ser mayor a 0.")

    # Simulación de Sobrecarga y Polimorfismo
    def calcular_costo(self, horas: int, descuento: float = 0.0) -> float:
        costo = (self.precio_base * horas) - descuento
        return max(0.0, costo)


class AlquilerEquipos(Servicio):
    def __init__(self, id_servicio, precio_base, requiere_seguro: bool):
        super().__init__(id_servicio, "Alquiler de Equipos", precio_base)
        self.requiere_seguro = requiere_seguro

    def validar_parametros(self):
        if self.precio_base < 0:
            raise ServicioNoDisponibleError("El precio base del equipo no puede ser negativo.")

    def calcular_costo(self, dias: int, impuesto: float = 0.19) -> float:
        costo_base = self.precio_base * dias
        if self.requiere_seguro:
            costo_base += 15000  # Costo fijo de seguro simulado
        return costo_base * (1 + impuesto)


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, precio_base, area: str):
        super().__init__(id_servicio, "Asesoría Especializada", precio_base)
        self.area = area

    def validar_parametros(self):
        if not self.area:
            raise ServicioNoDisponibleError("El área de asesoría no puede estar vacía.")

    def calcular_costo(self, horas: int, es_festivo: bool = False) -> float:
        factor = 1.5 if es_festivo else 1.0
        return self.precio_base * horas * factor


# --- Clase Controladora de Reservas ---

class Reserva:
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        # Bloques avanzados try/except/else/finally
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaInvalidaError("Objeto cliente no es válido.")
            if not isinstance(servicio, Servicio):
                raise ReservaInvalidaError("Objeto servicio no es válido.")
            if duracion <= 0:
                raise ReservaInvalidaError("La duración debe ser mayor a cero.")
        except ReservaInvalidaError as e:
            registrar_log("ERROR_RESERVA", str(e))
            raise e
        else:
            # Se ejecuta solo si no hubo excepciones en las condiciones previas
            self.id_reserva = id_reserva
            self.cliente = cliente
            self.servicio = servicio
            self.duracion = duracion
            self.estado = "Pendiente"
            registrar_log("INFO", f"Reserva {id_reserva} pre-creada con éxito.")

    def procesar_confirmacion(self, **kwargs):
        """Confirma la reserva calculando su costo dinámicamente."""
        try:
            # Polimorfismo en acción: calcula el costo según la subclase de servicio
            costo_final = self.servicio.calcular_costo(self.duracion, **kwargs)
            self.estado = "Confirmada"
            mensaje = f"Reserva {self.id_reserva} CONFIRMADA. Total a pagar: ${costo_final:.2f}"
            print(f"[ÉXITO] {mensaje}")
            registrar_log("TRANSACCION", mensaje)
        except Exception as e:
            # Encadenamiento de excepciones
            self.estado = "Fallida"
            error_msg = f"No se pudo confirmar la reserva {self.id_reserva} debido a parámetros de costo erróneos."
            registrar_log("ERROR_PROCESAMIENTO", error_msg)
            raise ReservaInvalidaError(error_msg) from e
