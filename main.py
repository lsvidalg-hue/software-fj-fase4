
# ------------------------------------------------------------
# CLASE GESTOR DEL SISTEMA
# ------------------------------------------------------------

class GestorSistema:
    """Administra clientes, servicios y reservas."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Cliente inválido.")

        self.clientes.append(cliente)
        logging.info("Cliente registrado correctamente.")

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Servicio inválido.")

        self.servicios.append(servicio)
        logging.info("Servicio registrado correctamente.")

    def registrar_reserva(self, reserva):
        if not isinstance(reserva, Reserva):
            raise ReservaInvalidaError("Reserva inválida.")

        self.reservas.append(reserva)
        logging.info("Reserva registrada correctamente.")

    def listar_clientes(self):
        for cliente in self.clientes:
            print(cliente.mostrar_informacion())

    def listar_servicios(self):
        for servicio in self.servicios:
            print(servicio.describir_servicio())

    def listar_reservas(self):
        for reserva in self.reservas:
            print(reserva.mostrar_informacion())


# ------------------------------------------------------------
# PRUEBAS DEL SISTEMA: 10 OPERACIONES
# ------------------------------------------------------------

def ejecutar_pruebas():
    """Ejecuta operaciones válidas e inválidas del sistema."""

    sistema = GestorSistema()

    print("\n========== PRUEBAS SOFTWARE FJ ==========\n")

    # OPERACIÓN 1: Registro válido de cliente
    try:
        cliente1 = Cliente(
            "C001",
            "Carlos Pérez",
            "carlos@gmail.com",
            "3001234567"
        )
        sistema.registrar_cliente(cliente1)
        print("1. Cliente registrado correctamente.")

    except Exception as error:
        logging.exception("Operación 1 fallida.")
        print("1. Error:", error)

    # OPERACIÓN 2: Registro de cliente inválido
    try:
        Cliente("C002", "", "correoincorrecto", "ABC")
    except DatosInvalidosError as error:
        logging.error("Operación 2: %s", error)
        print("2. Cliente inválido detectado:", error)

    # OPERACIÓN 3: Creación de reserva de sala
    try:
        sala = ReservaSala("S001", "Sala principal", 50000)
        sistema.registrar_servicio(sala)
        print("3. Servicio de sala creado correctamente.")

    except Exception as error:
        logging.exception("Operación 3 fallida.")
        print("3. Error:", error)

    # OPERACIÓN 4: Creación de alquiler de equipos
    try:
        equipo = AlquilerEquipo("E001", "Proyector", 30000)
        sistema.registrar_servicio(equipo)
        print("4. Servicio de equipos creado correctamente.")

    except Exception as error:
        logging.exception("Operación 4 fallida.")
        print("4. Error:", error)

    # OPERACIÓN 5: Creación de asesoría especializada
    try:
        asesoria = AsesoriaEspecializada(
            "A001", "Asesoría tecnológica", 80000
        )
        sistema.registrar_servicio(asesoria)
        print("5. Asesoría creada correctamente.")

    except Exception as error:
        logging.exception("Operación 5 fallida.")
        print("5. Error:", error)

    # OPERACIÓN 6: Creación de servicio con precio inválido
    try:
        ReservaSala("S002", "Sala secundaria", -5000)
    except DatosInvalidosError as error:
        logging.error("Operación 6: %s", error)
        print("6. Precio inválido detectado:", error)

    # OPERACIÓN 7: Reserva exitosa
    try:
        reserva1 = Reserva("R001", cliente1, sala, 2)
        sistema.registrar_reserva(reserva1)
        print("7. Reserva creada correctamente.")

    except Exception as error:
        logging.exception("Operación 7 fallida.")
        print("7. Error:", error)

    # OPERACIÓN 8: Intento de reserva con duración inválida
    try:
        Reserva("R002", cliente1, equipo, -2)
    except DatosInvalidosError as error:
        logging.error("Operación 8: %s", error)
        print("8. Duración inválida detectada:", error)

    # OPERACIÓN 9: Confirmación y procesamiento de reserva
    try:
        reserva1.confirmar()
        costo = reserva1.procesar()
        print("9. Reserva procesada. Costo: $", costo)

    except Exception as error:
        logging.exception("Operación 9 fallida.")
        print("9. Error:", error)

    # OPERACIÓN 10: Intento de procesar reserva cancelada
    try:
        reserva2 = Reserva("R003", cliente1, asesoria, 1)
        sistema.registrar_reserva(reserva2)
        reserva2.cancelar()
        reserva2.procesar()

    except ReservaInvalidaError as error:
        logging.error("Operación 10: %s", error)
        print("10. Error controlado:", error)

    finally:
        logging.info("Finalizaron las 10 operaciones de prueba.")

    print("\n========== RESUMEN DEL SISTEMA ==========")
    print("Clientes registrados:", len(sistema.clientes))
    print("Servicios registrados:", len(sistema.servicios))
    print("Reservas registradas:", len(sistema.reservas))
    print("\nPruebas finalizadas. Consulte software_fj.log.")

# ------------------------------------------------------------
# CLASE RESERVA
# ------------------------------------------------------------

class Reserva(Entidad):
    """Gestiona las reservas realizadas por los clientes."""

    def __init__(self, identificador, cliente, servicio, duracion):

        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Debe ingresar un cliente válido.")

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Debe seleccionar un servicio válido.")

        servicio.validar_parametros(duracion)

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"
        self.__fecha = datetime.now()

        logging.info(
            f"Reserva {identificador} creada correctamente."
        )

    @property
    def estado(self):
        return self.__estado

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    def confirmar(self):
        """Confirma una reserva pendiente."""

        if self.__estado != "Pendiente":
            raise ReservaInvalidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.__estado = "Confirmada"

        logging.info(
            f"Reserva {self.identificador} confirmada."
        )

        return "Reserva confirmada correctamente."

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""

        if self.__estado not in ["Pendiente", "Confirmada"]:
            raise ReservaInvalidaError(
                "La reserva no puede cancelarse."
            )

        self.__estado = "Cancelada"

        logging.info(
            f"Reserva {self.identificador} cancelada."
        )

        return "Reserva cancelada correctamente."

    def procesar(self):
        """Procesa la reserva y calcula el costo del servicio."""

        try:
            if self.__estado != "Confirmada":
                raise ReservaInvalidaError(
                    "La reserva debe estar confirmada para procesarse."
                )

            costo = self.__servicio.calcular_costo(
                self.__duracion
            )

        except ReservaInvalidaError as error:
            logging.error(
                f"Error al procesar reserva: {error}"
            )
            raise

        except Exception as error:
            logging.exception(
                "Error inesperado durante el procesamiento."
            )
            raise ErrorSistema(
                "No fue posible procesar la reserva."
            ) from error

        else:
            self.__estado = "Procesada"

            logging.info(
                f"Reserva {self.identificador} procesada. "
                f"Costo: ${costo:.2f}"
            )

            return costo

        finally:
            logging.info(
                f"Finalizó el intento de procesamiento "
                f"de reserva {self.identificador}."
            )

    def mostrar_informacion(self):
        return (
            f"Reserva: {self.identificador}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {self.__servicio.describir_servicio()}\n"
            f"Duración: {self.__duracion}\n"
            f"Estado: {self.__estado}\n"
            f"Fecha: {self.__fecha}"
        )

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

    logging.info("Sistema Software FJ iniciado.")

    try:
        ejecutar_pruebas()

    except Exception as error:
        logging.exception("Error general del sistema: %s", error)
        print("El sistema encontró un error:", error)

    finally:
        print("\nSistema Software FJ finalizado.")
        logging.info("Sistema finalizado.")
