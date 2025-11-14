from django.db import models

class Cooperativa(models.Model):
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=13, unique=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True)

    umbral_ocupacion = models.PositiveIntegerField(help_text="Porcentaje mínimo, ej: 60")
    porcentaje_comision = models.DecimalField(max_digits=5, decimal_places=2)
    ventana_inicio = models.TimeField()
    ventana_fin = models.TimeField()

    def __str__(self):
        return str(self.nombre)


class Bus(models.Model):
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE, related_name='buses')
    placa = models.CharField(max_length=10, unique=True)
    capacidad = models.PositiveIntegerField()

def __str__(self):
    return str(f"{self.placa} - {self.cooperativa.nombre}")




class Ruta(models.Model):
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE, related_name='rutas')
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    duracion_min = models.PositiveIntegerField(help_text="Duración en minutos")
    hora_salida = models.TimeField()

    def __str__(self):
        return str(f"{self.origen} → {self.destino} ({self.cooperativa.nombre})")



class Reserva(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='reservas')
    pasajero_nombre = models.CharField(max_length=100)
    pasajero_cedula = models.CharField(max_length=10)  # DATO SENSIBLE
    fecha_viaje = models.DateField()
    asiento = models.PositiveIntegerField()

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"Reserva {self.pasajero_nombre} - {self.bus.placa} ({self.fecha_viaje})")

