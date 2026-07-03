from abc import ABC, abstractmethod
from excepciones import ClienteInvalidoError, registrar_log

class EntidadSistema(ABC):
    """Clase abstracta que representa entidades generales del sistema."""
    @abstractmethod
    def obtener_detalles(self) -> str:
        pass

class Cliente(EntidadSistema):
    """Clase Cliente con encapsulamiento estricto."""
    def __init__(self, id_cliente: str, nombre: str, correo: str):
        # Validaciones robustas en el constructor
        if not id_cliente or not nombre or "@" not in correo:
            error_msg = f"Datos de cliente inválidos: ID={id_cliente}, Nombre={nombre}, Correo={correo}"
            registrar_log("ERROR_VALIDACION", error_msg)
            raise ClienteInvalidoError(error_msg)
            
        self.__id_cliente = id_cliente  # Atributo privado
        self.__nombre = nombre          # Atributo privado
        self.__correo = correo          # Atributo privado
        registrar_log("INFO", f"Cliente creado con éxito: {self.__nombre}")

    # Getters para mantener la encapsulación
    @property
    def id_cliente(self):
        return self.__id_cliente

    @property
    def nombre(self):
        return self.__nombre

    def obtener_detalles(self) -> str:
        return f"Cliente: {self.__nombre} (ID: {self.__id_cliente})"


class Servicio(ABC):
    """Clase abstracta Base para los Servicios de la empresa."""
    def __init__(self, id_servicio: str, nombre_servicio: str, precio_base: float):
        self.id_servicio = id_servicio
        self.nombre_servicio = nombre_servicio
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método abstracto para implementar polimorfismo."""
        pass

    @abstractmethod
    def validar_parametros(self) -> bool:
        """Valida que las condiciones específicas del servicio se cumplan."""
        pass
