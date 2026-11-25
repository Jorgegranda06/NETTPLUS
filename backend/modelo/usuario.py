from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    nombre: str
    usuario: str
    rol: str
    activo: int = 1

    @classmethod
    def desde_fila(cls, fila):
        return cls(**{k: fila[k] for k in ('id', 'nombre', 'usuario', 'rol', 'activo')})

    def publico(self):
        return {'id': self.id, 'nombre': self.nombre, 'usuario': self.usuario, 'rol': self.rol, 'activo': self.activo}
