from dataclasses import dataclass

@dataclass
class Marcacion:
    empleado_id: str
    nombre: str
    departamento_id: str
    departamento: str
    cargo_id: str
    fecha: str
    hora: str
    tipo_marcacion: str
    tipo: str
    fuente: str
