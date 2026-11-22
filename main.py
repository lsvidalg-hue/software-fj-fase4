
# ------------------------------------------------------------
# CLASE ABSTRACTA SERVICIO
# ------------------------------------------------------------

class Servicio(Entidad, ABC):
    """Clase base para los servicios de Software FJ."""

    def __init__(self, identificador, nombre, precio_base):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")

        if not isinstance(precio_base, (int, float)) or isinstance(precio_base, bool) or precio_base <= 0:
            raise DatosInvalidosError("El precio debe ser mayor que cero.")

        self._nombre = nombre
        self._precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass


# ------------------------------------------------------------
# SERVICIO 1: RESERVA DE SALAS
# ------------------------------------------------------------

class ReservaSala(Servicio):

    def mostrar_informacion(self):
        return self.describir_servicio()

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración de la sala debe ser positiva.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self._precio_base * duracion
        return subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

    def describir_servicio(self):
        return f"Reserva de sala: {self._nombre}"


# ------------------------------------------------------------
# SERVICIO 2: ALQUILER DE EQUIPOS
# ------------------------------------------------------------

class AlquilerEquipo(Servicio):

    def mostrar_informacion(self):
        return self.describir_servicio()

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración del alquiler debe ser positiva.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self._precio_base * duracion
        return subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

    def describir_servicio(self):
        return f"Alquiler de equipos: {self._nombre}"


# ------------------------------------------------------------
# SERVICIO 3: ASESORÍAS ESPECIALIZADAS
# ------------------------------------------------------------

class AsesoriaEspecializada(Servicio):

    def mostrar_informacion(self):
        return self.describir_servicio()

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración de la asesoría debe ser positiva.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self._precio_base * duracion
        return subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

    def describir_servicio(self):
        return f"Asesoría especializada: {self._nombre}"

# ------------------------------------------------------------
# CLASE CLIENTE
# ------------------------------------------------------------

class Cliente(Entidad):
    """Representa un cliente registrado en Software FJ."""

    def __init__(self, identificador, nombre, correo, telefono):

        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del cliente es obligatorio.")

        if not isinstance(correo, str) or "@" not in correo:
            raise DatosInvalidosError("El correo electrónico no es válido.")

        if not isinstance(telefono, str) or not telefono.isdigit():
            raise DatosInvalidosError("El teléfono debe contener solo números.")

        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_informacion(self):
        return (
            f"ID: {self.identificador} | "
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )
# ============================================================
# PROYECTO: SOFTWARE FJ
# Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Curso: Programación - UNAD
# Fase 4: Manejo de excepciones
# ============================================================

from abc import ABC, abstractmethod
import logging
from datetime import datetime

# ------------------------------------------------------------
# CONFIGURACIÓN DEL REGISTRO DE EVENTOS Y ERRORES
# ------------------------------------------------------------

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ------------------------------------------------------------
# EXCEPCIONES PERSONALIZADAS
# ------------------------------------------------------------

class ErrorSistema(Exception):
    """Excepción general del sistema Software FJ."""
    pass


class DatosInvalidosError(ErrorSistema):
    """Se presenta cuando los datos ingresados no son válidos."""
    pass


class ServicioNoDisponibleError(ErrorSistema):
    """Se presenta cuando un servicio no está disponible."""
    pass


class ReservaInvalidaError(ErrorSistema):
    """Se presenta cuando una reserva no cumple los requisitos."""
    pass


# ------------------------------------------------------------
# CLASE ABSTRACTA: ENTIDAD
# ------------------------------------------------------------

class Entidad(ABC):
    """Representa las entidades generales del sistema."""

    def __init__(self, identificador):
        if not identificador:
            raise DatosInvalidosError(
                "El identificador es obligatorio."
            )

        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        """Método que implementarán las clases derivadas."""
        pass


# ------------------------------------------------------------
# INICIO DEL SISTEMA
# ------------------------------------------------------------

if __name__ == "__main__":
    print("======================================")
    print("       BIENVENIDO A SOFTWARE FJ")
    print(" Sistema de Gestión de Clientes y")
    print("       Servicios y Reservas")
    print("======================================")

    logging.info("Sistema Software FJ iniciado correctamente.")
