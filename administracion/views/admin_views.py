from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from administracion.models import Cooperativa, Bus, Reserva

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


# Admin Home
def panel_home(request):
    return render(request, 'administracion/panel_home.html')


# Cooperativas
class CooperativaListView(AdminRequiredMixin, ListView):
    model = Cooperativa
    template_name = 'administracion/cooperativa_list.html'


class CooperativaCreateView(AdminRequiredMixin, CreateView):
    model = Cooperativa
    fields = [
        'nombre', 'ruc', 'correo', 'telefono',
        'umbral_ocupacion', 'porcentaje_comision',
        'ventana_inicio', 'ventana_fin'
    ]
    template_name = 'administracion/cooperativa_form.html'
    success_url = reverse_lazy('cooperativa_list')


# Buses
class BusListView(AdminRequiredMixin, ListView):
    model = Bus
    template_name = 'administracion/bus_list.html'


class BusCreateView(AdminRequiredMixin, CreateView):
    model = Bus
    fields = ['cooperativa', 'placa', 'capacidad']
    template_name = 'administracion/bus_form.html'
    success_url = reverse_lazy('bus_list')


# monitoreo
from django.db.models import Count, F, FloatField, ExpressionWrapper
from django.shortcuts import render

class MonitoreoView(AdminRequiredMixin, ListView):
    model = Bus
    template_name = 'administracion/monitoreo.html'

    def get_queryset(self):
        return Bus.objects.annotate(
            reservas_count=Count('reservas'),
            ocupacion=ExpressionWrapper(
                100.0 * Count('reservas') / F('capacidad'),
                output_field=FloatField()
            )
        )
