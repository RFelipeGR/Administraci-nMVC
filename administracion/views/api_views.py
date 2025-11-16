from django.http import JsonResponse
from administracion.models import Bus

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