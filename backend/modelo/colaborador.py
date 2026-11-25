from dataclasses import dataclass

@dataclass
class Colaborador:
    empleado_id: str
    nombre: str
    departamento: str = ''
    cargo_id: str = ''
    # Modelo preliminar; datos laborales reales requieren archivo maestro de la empresa.
