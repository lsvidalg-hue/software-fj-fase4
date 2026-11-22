
# ============================================================
# PROYECTO: SOFTWARE FJ
# Sistema Integral de Clientes, Servicios y Reservas
# UNAD - Curso Programacion - Fase 4
# ============================================================

from abc import ABC, abstractmethod
import logging
from datetime import datetime

# ============================================================
# CONFIGURACION DE LOGS
# ============================================================

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ============================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================

class ErrorSistema(Exception):
    pass


class DatosInvalidosError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class ReservaInvalidaError(ErrorSistema):
    pass


# ============================================================
# CLASE ABSTRACTA ENTIDAD
# ============================================================

class Entidad(ABC):

    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError("Identificador obligatorio.")

        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ============================================================
# CLASE CLIENTE
# ============================================================

class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("Nombre obligatorio.")

        if not isinstance(correo, str) or "@" not in correo:
            raise DatosInvalidosError("Correo invalido.")

        if not isinstance(telefono, str) or not telefono.isdigit():
            raise DatosInvalidosError("Telefono invalido.")

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
            f"Cliente: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Telefono: {self.__telefono}"
        )


# ============================================================
# CLASE ABSTRACTA SERVICIO
# ============================================================

class Servicio(Entidad, ABC):

    def __init__(self, identificador, nombre, precio_base):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("Nombre del servicio obligatorio.")

        if (isinstance(precio_base, bool) or
                not isinstance(precio_base, (int, float)) or
                precio_base <= 0):
            raise DatosInvalidosError("Precio invalido.")

        self._nombre = nombre.strip()
        self._precio_base = precio_base

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)

        if not 0 <= descuento <= 100:
            raise DatosInvalidosError("Descuento invalido.")

        if not 0 <= impuesto <= 100:
            raise DatosInvalidosError("Impuesto invalido.")

        subtotal = self._precio_base * duracion
        return subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass


# ============================================================
# SERVICIO 1: RESERVA DE SALAS
# ============================================================

class ReservaSala(Servicio):

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("Duracion de sala invalida.")

    def describir_servicio(self):
        return f"Reserva de sala: {self._nombre}"

    def mostrar_informacion(self):
        return self.describir_servicio()


# ============================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# ============================================================

class AlquilerEquipo(Servicio):

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("Duracion de alquiler invalida.")

    def describir_servicio(self):
        return f"Alquiler de equipos: {self._nombre}"

    def mostrar_informacion(self):
        return self.describir_servicio()


# ============================================================
# SERVICIO 3: ASESORIAS ESPECIALIZADAS
# ============================================================

class AsesoriaEspecializada(Servicio):

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("Duracion de asesoria invalida.")

    def describir_servicio(self):
        return f"Asesoria especializada: {self._nombre}"

    def mostrar_informacion(self):
        return self.describir_servicio()


# ============================================================
# CLASE RESERVA
# ============================================================

class Reserva(Entidad):

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Cliente invalido.")

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Servicio invalido.")

        servicio.validar_parametros(duracion)

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"
        self.__fecha = datetime.now()

        logging.info("Reserva %s creada.", identificador)

    @property
    def estado(self):
        return self.__estado

    def confirmar(self):
        if self.__estado != "Pendiente":
            raise ReservaInvalidaError("La reserva no esta pendiente.")

        self.__estado = "Confirmada"
        logging.info("Reserva %s confirmada.", self.identificador)

    def cancelar(self):
        if self.__estado not in ("Pendiente", "Confirmada"):
            raise ReservaInvalidaError("No se puede cancelar esta reserva.")

        self.__estado = "Cancelada"
        logging.info("Reserva %s cancelada.", self.identificador)

    def procesar(self):
        try:
            if self.__estado != "Confirmada":
                raise ReservaInvalidaError(
                    "La reserva debe estar confirmada."
                )

            costo = self.__servicio.calcular_costo(self.__duracion)

        except ReservaInvalidaError as error:
            logging.error("Error de reserva: %s", error)
            raise

        except Exception as error:
            logging.exception("Error inesperado al procesar reserva.")
            raise ErrorSistema("Fallo en el procesamiento.") from error

        else:
            self.__estado = "Procesada"
            logging.info("Reserva procesada. Costo: %.2f", costo)
            return costo

        finally:
            logging.info("Finalizo intento de procesamiento: %s",
                         self.identificador)

    def mostrar_informacion(self):
        return (
            f"Reserva: {self.identificador}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {self.__servicio.describir_servicio()}\n"
            f"Duracion: {self.__duracion}\n"
            f"Estado: {self.__estado}\n"
            f"Fecha: {self.__fecha}"
        )


# ============================================================
# GESTOR DEL SISTEMA
# ============================================================

class GestorSistema:

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Cliente invalido.")

        self.clientes.append(cliente)
        logging.info("Cliente registrado.")

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Servicio invalido.")

        self.servicios.append(servicio)
        logging.info("Servicio registrado.")

    def registrar_reserva(self, reserva):
        if not isinstance(reserva, Reserva):
            raise ReservaInvalidaError("Reserva invalida.")

        self.reservas.append(reserva)
        logging.info("Reserva registrada.")


# ============================================================
# DIEZ OPERACIONES DE PRUEBA
# ============================================================

def ejecutar_pruebas():

    sistema = GestorSistema()

    print("\n========== SOFTWARE FJ ==========\n")

    # OPERACION 1: Registro valido de cliente
    try:
        cliente = Cliente("C001", "Carlos Perez",
                          "carlos@gmail.com", "3001234567")
        sistema.registrar_cliente(cliente)
        print("1. Cliente registrado correctamente.")
    except ErrorSistema as error:
        logging.error("Operacion 1: %s", error)
        print("1. Error:", error)

    # OPERACION 2: Registro invalido
    try:
        Cliente("C002", "", "correo", "ABC")
    except ErrorSistema as error:
        logging.error("Operacion 2: %s", error)
        print("2. Cliente invalido detectado.")

    # OPERACION 3: Crear sala
    try:
        sala = ReservaSala("S001", "Sala principal", 50000)
        sistema.registrar_servicio(sala)
        print("3. Sala creada correctamente.")
    except ErrorSistema as error:
        print("3. Error:", error)

    # OPERACION 4: Crear alquiler de equipos
    try:
        equipo = AlquilerEquipo("E001", "Proyector", 30000)
        sistema.registrar_servicio(equipo)
        print("4. Alquiler de equipos creado.")
    except ErrorSistema as error:
        print("4. Error:", error)

    # OPERACION 5: Crear asesoria
    try:
        asesoria = AsesoriaEspecializada(
            "A001", "Asesoria tecnologica", 80000)
        sistema.registrar_servicio(asesoria)
        print("5. Asesoria creada correctamente.")
    except ErrorSistema as error:
        print("5. Error:", error)

    # OPERACION 6: Precio invalido
    try:
        ReservaSala("S002", "Sala secundaria", -5000)
    except ErrorSistema as error:
        logging.error("Operacion 6: %s", error)
        print("6. Precio invalido detectado.")

    # OPERACION 7: Crear reserva
    try:
        reserva1 = Reserva("R001", cliente, sala, 2)
        sistema.registrar_reserva(reserva1)
        print("7. Reserva creada correctamente.")
    except ErrorSistema as error:
        print("7. Error:", error)

    # OPERACION 8: Duracion invalida
    try:
        Reserva("R002", cliente, equipo, -2)
    except ErrorSistema as error:
        logging.error("Operacion 8: %s", error)
        print("8. Duracion invalida detectada.")

    # OPERACION 9: Confirmar y procesar reserva
    try:
        reserva1.confirmar()
        costo = reserva1.procesar()
        print(f"9. Reserva procesada. Costo: ${costo:,.2f}")
    except ErrorSistema as error:
        logging.error("Operacion 9: %s", error)
        print("9. Error:", error)

    # OPERACION 10: Intentar procesar reserva cancelada
    try:
        reserva2 = Reserva("R003", cliente, asesoria, 1)
        sistema.registrar_reserva(reserva2)
        reserva2.cancelar()
        reserva2.procesar()

    except ReservaInvalidaError as error:
        logging.error("Operacion 10: %s", error)
        print("10. Error controlado:", error)

    finally:
        logging.info("Finalizaron las diez operaciones.")

    print("\n========== RESUMEN ==========")
    print("Clientes:", len(sistema.clientes))
    print("Servicios:", len(sistema.servicios))
    print("Reservas:", len(sistema.reservas))
    print("\nConsulte el archivo software_fj.log.")


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================

if __name__ == "__main__":

    print("BIENVENIDO A SOFTWARE FJ")

    try:
        ejecutar_pruebas()

    except Exception as error:
        logging.exception("Error general: %s", error)
        print("Error general del sistema:", error)

    finally:
        print("\nSistema finalizado.")

