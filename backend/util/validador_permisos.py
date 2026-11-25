from datetime import datetime, date, time
from modelo.solicitud import Solicitud

class ValidadorPermisos:
    COLUMNAS=('ID del Empleado','Nombres','Apellidos','nombre de empresa','Departamento',
              'Hora Entrada','Hora Salida','Motivo de Aprobación','Hora','Código de pago',
              'Estado de aprobación','Comentarios de aprobación','Aprobador')

    def indices(self, encabezado):
        posiciones={str(c or '').strip().casefold():i for i,c in enumerate(encabezado or [])}
        faltantes=[c for c in self.COLUMNAS if c.casefold() not in posiciones]
        if faltantes: raise ValueError('Columnas faltantes: '+', '.join(faltantes))
        return {c:posiciones[c.casefold()] for c in self.COLUMNAS}

    @staticmethod
    def fecha(v, obligatoria=True):
        if isinstance(v,datetime): return v
        if isinstance(v,date): return datetime.combine(v,time.min)
        if v is None or not str(v).strip():
            if obligatoria: raise ValueError('Fecha obligatoria vacía')
            return None
        try: return datetime.fromisoformat(str(v).strip())
        except ValueError as exc: raise ValueError('Fecha inválida') from exc

    def convertir(self,fila,idx):
        def leer(c):
            v=fila[idx[c]] if idx[c]<len(fila) else None
            return str(v).strip() if v is not None else ''
        emp=leer('ID del Empleado')
        if not emp: raise ValueError('Falta ID del Empleado')
        inicio=self.fecha(fila[idx['Hora Entrada']]);fin=self.fecha(fila[idx['Hora Salida']])
        if fin<inicio: raise ValueError('Salida anterior a entrada')
        return Solicitud(emp,leer('Nombres'),leer('Apellidos'),leer('nombre de empresa'),
          leer('Departamento'),inicio,fin,leer('Motivo de Aprobación'),
          self.fecha(fila[idx['Hora']],False),leer('Código de pago'),
          leer('Estado de aprobación'),leer('Comentarios de aprobación'),leer('Aprobador'))
