from dataclasses import dataclass

@dataclass
class Horario:
    empleado_id: str
    entrada: str
    salida: str
    # No se persiste todavía: pendiente de conocer el formato oficial.
