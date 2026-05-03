import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings # Para traer el DOMAIN que pusimos arriba

class Patente(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente de Revisión'),
        ('aprobado', 'Listo para Retiro/Impresión'),
        ('rechazado', 'Documento Inválido'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_patente = models.CharField(max_length=20)
    pdf_documento = models.FileField(upload_to='patentes/pdfs/')
    qr_imagen = models.ImageField(upload_to='patentes/qrs/', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    fecha_validacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.numero_patente} - {self.cliente.username}"

    def save(self, *args, **kwargs):
        # Si apruebas el documento, se pone la hora actual y se genera el QR
        if self.estado == 'aprobado':
            if not self.fecha_validacion:
                self.fecha_validacion = timezone.now()
            if not self.qr_imagen:
                self.generar_qr_con_texto()
        super().save(*args, **kwargs)

    def generar_qr_con_texto(self):
        # 1. Creamos la URL dinámica usando el dominio de settings[cite: 6, 7]
        dominio = getattr(settings, 'DOMAIN', 'http://127.0.0.1:8000')
        url_archivo = f"{dominio}{self.pdf_documento.url}"

        # 2. Generar el código QR básico[cite: 6]
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url_archivo)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # 3. Preparar el lienzo con espacio extra abajo para la patente
        ancho, alto = qr_img.size
        margen_texto = 60
        imagen_final = Image.new('RGB', (ancho, alto + margen_texto), 'white')
        imagen_final.paste(qr_img, (0, 0))

        # 4. Dibujar el número de patente abajo
        draw = ImageDraw.Draw(imagen_final)
        
        # Intentamos cargar fuentes comunes (Windows o Linux)[cite: 6]
        try:
            # En Windows 'arial.ttf', en Linux 'DejaVuSans.ttf'
            font = ImageFont.truetype("arial.ttf", 26) 
        except:
            font = ImageFont.load_default()

        texto = self.numero_patente.upper()
        # Calculamos para que quede centradito
        bbox = draw.textbbox((0, 0), texto, font=font)
        ancho_t = bbox[2] - bbox[0]
        pos_x = (ancho - ancho_t) / 2
        
        draw.text((pos_x, alto - 5), texto, fill="black", font=font)

        # 5. Guardar en el campo ImageField (compatible con local y Firebase)[cite: 6, 7]
        buffer = BytesIO()
        imagen_final.save(buffer, format='PNG')
        self.qr_imagen.save(f"qr_{self.numero_patente}.png", File(buffer), save=False)