import datetime

# Excepciones personalizadas
class ErrorSoftwareFJ(Exception):
    """Excepción base para el sistema."""
    pass

class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos del cliente no cumplen las validaciones."""
    pass

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio no está disponible o sus datos son erróneos."""
    pass

class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando hay conflictos con las reservas (fechas, duraciones, etc.)."""
    pass

def registrar_log(tipo_evento, mensaje):
    """Registra de manera síncrona los eventos y errores en un archivo físico."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] [{tipo_evento}] - {mensaje}\n"
    
    # Uso de bloques try/except/finally para manejo seguro de archivos
    try:
        with open("errores.log", "a", encoding="utf-8") as archivo:
            archivo.write(linea)
    except IOError as e:
        print(f"Error crítico de I/O al intentar escribir en el log: {e}")
    finally:
        # Asegura que el flujo de consola se mantenga limpio
        pass
