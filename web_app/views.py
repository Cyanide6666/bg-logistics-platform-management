from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PatenteForm
from .models import Patente

def home(request):
    return render(request, 'home.html')

# views.py
@login_required
def panel_cliente(request):
    # El signo - antes de fecha_subida ordena de forma descendente
    mis_patentes = Patente.objects.filter(cliente=request.user).order_by('-fecha_subida')

    if request.method == 'POST':
        form = PatenteForm(request.POST, request.FILES) 
        if form.is_valid():
            nueva_patente = form.save(commit=False)
            nueva_patente.cliente = request.user
            nueva_patente.save() # Aquí es donde fallaría si la DB sigue bloqueada
            return redirect('panel_cliente')
    else:
        form = PatenteForm()
    
    return render(request, 'cliente/panel.html', {'mis_patentes': mis_patentes, 'form': form})