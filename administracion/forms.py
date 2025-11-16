from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Reserva

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['bus', 'pasajero_nombre', 'pasajero_cedula', 'fecha_viaje', 'asiento']
        widgets = {
            'fecha_viaje': forms.DateInput(attrs={'type': 'date'}),
        }

    # VALIDACIÓN: evita reservar asiento repetido
    def clean(self):
        cleaned = super().clean()
        bus = cleaned.get('bus')
        fecha = cleaned.get('fecha_viaje')
        asiento = cleaned.get('asiento')

        if bus and fecha and asiento:
            existe = bus.reservas.filter(
                fecha_viaje=fecha,
                asiento=asiento
            ).exists()

            if existe:
                raise forms.ValidationError("Ese asiento ya está reservado para esa fecha.")

        return cleaned
