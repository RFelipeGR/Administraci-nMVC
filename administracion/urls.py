from django.urls import path
from administracion.views.auth_views import login_view, logout_view
from administracion.views.admin_views import (
    panel_home,
    CooperativaListView, CooperativaCreateView,
    BusListView, BusCreateView,
    MonitoreoView
)
from administracion.views.usuario_views import (
    usuario_home,
    ReservaListView, ReservaCreateView
)
from administracion.views.api_views import buses_por_cooperativa


urlpatterns = [
    # Auth
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Inicio
    path('', panel_home, name='panel_home'),
    path('usuario/', usuario_home, name='usuario_home'),

    # Cooperativas
    path('cooperativas/', CooperativaListView.as_view(), name='cooperativa_list'),
    path('cooperativas/nuevo/', CooperativaCreateView.as_view(), name='cooperativa_create'),

    # Buses
    path('buses/', BusListView.as_view(), name='bus_list'),
    path('buses/nuevo/', BusCreateView.as_view(), name='bus_create'),

    # Reservas
    path('reservas/', ReservaListView.as_view(), name='reserva_list'),
    path('reservas/nuevo/', ReservaCreateView.as_view(), name='reserva_create'),

    # API
    path('api/buses/', buses_por_cooperativa, name='api_buses_por_cooperativa'),

    # Monitoreo
    path('monitoreo/', MonitoreoView.as_view(), name='monitoreo'),
]
