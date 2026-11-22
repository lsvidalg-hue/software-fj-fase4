
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
