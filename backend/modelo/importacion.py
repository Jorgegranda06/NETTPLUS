from dataclasses import dataclass, field

@dataclass
class ResultadoImportacion:
    total: int = 0
    insertados: int = 0
    duplicados: int = 0
    rechazados: int = 0
    errores: list = field(default_factory=list)

    def publico(self):
        return {'mensaje': 'Importación procesada', 'total': self.total,
                'insertados': self.insertados, 'duplicados': self.duplicados,
                'rechazados': self.rechazados, 'errores': self.errores}
