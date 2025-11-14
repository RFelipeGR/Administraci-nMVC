from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Cooperativa, Bus, Ruta, Reserva
from .forms import ReservaForm
from django.http import JsonResponse
from django.db.models import Count, F, FloatField, ExpressionWrapper
from django.views.generic import ListView
from .models import Bus


class CooperativaListView(ListView):
    model = Cooperativa
    template_name = 'administracion/cooperativa_list.html'


class CooperativaCreateView(CreateView):
    model = Cooperativa
    fields = ['nombre', 'ruc', 'correo', 'telefono',
              'umbral_ocupacion', 'porcentaje_comision',
              'ventana_inicio', 'ventana_fin']
    template_name = 'administracion/cooperativa_form.html'
    success_url = reverse_lazy('cooperativa_list')


class BusListView(ListView):
    model = Bus
    template_name = 'administracion/bus_list.html'


class BusCreateView(CreateView):
    model = Bus
    fields = ['cooperativa', 'placa', 'capacidad']
    template_name = 'administracion/bus_form.html'
    success_url = reverse_lazy('bus_list')


class ReservaListView(ListView):
    model = Reserva
    template_name = 'administracion/reserva_list.html'


class ReservaCreateView(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'administracion/reserva_form.html'
    success_url = reverse_lazy('reserva_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cooperativas'] = Cooperativa.objects.all()
        return context



def buses_por_cooperativa(request):
    cooperativa_id = request.GET.get('cooperativa_id')
    data = []
    if cooperativa_id:
        buses = Bus.objects.filter(cooperativa_id=cooperativa_id).order_by('placa')
        data = [
            {'id': bus.id, 'texto': f"{bus.placa} (cap: {bus.capacidad})"}
            for bus in buses
        ]
    return JsonResponse({'buses': data})



from django.db.models import Count, F, FloatField, ExpressionWrapper
from django.views.generic import ListView
from .models import Bus

class MonitoreoView(ListView):
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
