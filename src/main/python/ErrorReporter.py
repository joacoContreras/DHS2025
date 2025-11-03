class Error:
    "Clase para representar un error"
    def __init__(self, tipo, linea, mensaje):
        self.tipo = tipo  # "SINTÁCTICO" o "SEMÁNTICO"
        self.linea = linea
        self.mensaje = mensaje
    
    def __str__(self):
        return f"[{self.tipo}] Línea {self.linea}: {self.mensaje}"


class ErrorReporter:
    "Singleton para reportar errores sintácticos y semánticos"
    _instance = None
    
    def __init__(self):
        self.errores = []
        self.tiene_errores = False
    
    @staticmethod
    def getInstance():
        if ErrorReporter._instance is None:
            ErrorReporter._instance = ErrorReporter()
        return ErrorReporter._instance
    
    def reset(self):
        """Reinicia el reporte de errores"""
        self.errores = []
        self.tiene_errores = False
    
    def reportarErrorSintactico(self, linea, mensaje):
        """Reporta un error sintáctico"""
        error = Error("SINTÁCTICO", linea, mensaje)
        self.errores.append(error)
        self.tiene_errores = True
        print(f" {error}")
    
    def reportarErrorSemantico(self, linea, mensaje):
        """Reporta un error semántico"""
        error = Error("SEMÁNTICO", linea, mensaje)
        self.errores.append(error)
        self.tiene_errores = True
        print(f" {error}")
    
    def tieneErrores(self):
        """Retorna True si hay errores"""
        return self.tiene_errores
    
    def obtenerErrores(self):
        """Retorna la lista de errores"""
        return self.errores
    
    def generarReporte(self, archivo=None):
        """Genera un reporte de errores"""
        if not self.tiene_errores:
            mensaje = " No se encontraron errores.\n"
            if archivo:
                with open(archivo, 'w') as f:
                    f.write(mensaje)
            else:
                print(mensaje)
            return
        
        # Separar errores por tipo
        sintacticos = [e for e in self.errores if e.tipo == "SINTÁCTICO"]
        semanticos = [e for e in self.errores if e.tipo == "SEMÁNTICO"]
        
        reporte = []
        reporte.append("=" * 60)
        reporte.append("         REPORTE DE ERRORES")
        reporte.append("=" * 60)
        reporte.append(f"Total de errores: {len(self.errores)}")
        reporte.append(f"  • Errores sintácticos: {len(sintacticos)}")
        reporte.append(f"  • Errores semánticos: {len(semanticos)}")
        reporte.append("=" * 60)
        
        if sintacticos:
            reporte.append("\n ERRORES SINTÁCTICOS:")
            reporte.append("-" * 60)
            for error in sintacticos:
                reporte.append(f"  {error}")
        
        if semanticos:
            reporte.append("\n ERRORES SEMÁNTICOS:")
            reporte.append("-" * 60)
            for error in semanticos:
                reporte.append(f"  {error}")
        
        reporte.append("\n" + "=" * 60)
        
        reporte_texto = "\n".join(reporte)
        
        if archivo:
            with open(archivo, 'w') as f:
                f.write(reporte_texto)
            print(f"\nReporte guardado en: {archivo}")
        else:
            print(reporte_texto)
    
    def __str__(self):
        return f"ErrorReporter: {len(self.errores)} errores"
