from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from administracion.models import Reserva, Cooperativa
from administracion.forms import ReservaForm


# User home
def usuario_home(request):
    return render(request, 'administracion/usuario_home.html')


# Reservas list
class ReservaListView(ListView):
    model = Reserva
    template_name = 'administracion/reserva_list.html'


# Reservas Creación
class ReservaCreateView(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'administracion/reserva_form.html'
    success_url = reverse_lazy('reserva_list')

    # Pasar cooperativas al formulario (dropdown dinámico)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cooperativas'] = Cooperativa.objects.all()
        return context