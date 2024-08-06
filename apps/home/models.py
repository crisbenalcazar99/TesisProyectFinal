from django.db import models


class RegistroTemperatura(models.Model):
    temperatura = models.FloatField()
    humedad = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Registro {self.id} - Temp: {self.temperatura}, Humedad: {self.humedad}"


class RegistroUbicacion(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Registro {self.id} - Temp: {self.temperatura}, Humedad: {self.humedad}"


class RegistroImagen(models.Model):
    contiene_varroa = models.BooleanField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Registro {self.id} - {self.fecha_registro}"
