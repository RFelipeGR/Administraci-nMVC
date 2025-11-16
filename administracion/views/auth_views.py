from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)

        if user.is_staff:
            return redirect('/panel/')
        else:
            return redirect('/panel/usuario/')

    return render(request, 'administracion/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/panel/login/')