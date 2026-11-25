from datetime import datetime
from modelo.marcacion import Marcacion

class ValidadorExcel:
    HEADERS = ['Id del Empleado','Nombres','ID de Departamento','Departamento',
               'ID del Cargo','Fecha','Hora','Tipo de Marcación','Tipo','Fuente de Datos']

    @staticmethod
    def fecha(valor):
        if isinstance(valor, datetime):
            return valor.strftime('%Y-%m-%d')
        cadena = str(valor or '').strip()
        for formato in ('%d-%m-%Y','%d/%m/%Y','%Y-%m-%d','%Y/%m/%d'):
            try:
                return datetime.strptime(cadena, formato).strftime('%Y-%m-%d')
            except ValueError:
                pass
        raise ValueError('Fecha inválida')

    @staticmethod
    def hora(valor):
        if hasattr(valor, 'strftime') and not isinstance(valor, str):
            return valor.strftime('%H:%M:%S')
        cadena = str(valor or '').strip()
        for formato in ('%H:%M:%S','%H:%M'):
            try:
                return datetime.strptime(cadena, formato).strftime('%H:%M:%S')
            except ValueError:
                pass
        raise ValueError('Hora inválida')

    def indices(self, encabezados):
        actuales = [str(v or '').strip() for v in (encabezados or [])]
        faltantes = [h for h in self.HEADERS if h not in actuales]
        if faltantes:
            raise ValueError('Faltan columnas obligatorias: ' + ', '.join(faltantes))
        return {h: actuales.index(h) for h in self.HEADERS}

    def convertir_marcacion(self, fila, indices):
        datos = {h: fila[indices[h]] if indices[h] < len(fila) else None for h in self.HEADERS}
        emp = str(datos['Id del Empleado'] or '').strip()
        nombre = str(datos['Nombres'] or '').strip()
        if not emp or not nombre:
            raise ValueError('Falta identificador o nombre')
        tipo = str(datos['Tipo de Marcación'] or '').strip().title()
        if tipo not in ('Entrada', 'Salida'):
            raise ValueError('Tipo de marcación inválido')
        return Marcacion(emp, nombre, str(datos['ID de Departamento'] or ''),
                         str(datos['Departamento'] or ''), str(datos['ID del Cargo'] or ''),
                         self.fecha(datos['Fecha']), self.hora(datos['Hora']), tipo,
                         str(datos['Tipo'] or ''), str(datos['Fuente de Datos'] or ''))
