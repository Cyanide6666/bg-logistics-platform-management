from django.contrib import admin
from .models import Patente

@admin.register(Patente)
class PatenteAdmin(admin.ModelAdmin):
    # Esto define qué columnas verás en la lista del admin
    list_display = ('numero_patente', 'cliente', 'estado', 'fecha_subida')
    
    # Esto crea un filtro a la derecha para ver solo las "pendientes"
    list_filter = ('estado', 'fecha_subida')
    
    # Esto te permite buscar por número de patente o nombre de usuario
    search_fields = ('numero_patente', 'cliente__username')

    # Esto hará que las más nuevas aparezcan arriba de todo
    ordering = ('-fecha_subida',)
    
    # Esto hace que puedas cambiar el estado directamente en el admin
    list_editable = ('estado',)

