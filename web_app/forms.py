from django import forms
from .models import Patente

class PatenteForm(forms.ModelForm):
    class Meta:
        model = Patente
        fields = ['numero_patente', 'pdf_documento']
