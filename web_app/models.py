from django.db import models
from django.contrib.auth.models import User

class Patente(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente de Revisión'),
        ('aprobado', 'Listo para Retiro/Impresión'),
        ('rechazado', 'Documento Inválido'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_patente = models.CharField(max_length=20, unique=False)
    pdf_documento = models.FileField(upload_to='patentes/pdfs/')
    qr_imagen = models.ImageField(upload_to='patentes/qrs/', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    fecha_validacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.numero_patente} - {self.cliente.username}"