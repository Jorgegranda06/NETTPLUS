from dataclasses import dataclass
from datetime import datetime

@dataclass
class Solicitud:
    empleado_id: str
    nombres: str
    apellidos: str
    empresa: str
    departamento: str
    fecha_inicio: datetime
    fecha_fin: datetime
    motivo: str
    fecha_aprobacion: datetime | None
    codigo_pago: str
    estado: str
    comentario: str
    aprobador: str
