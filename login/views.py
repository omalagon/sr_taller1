from django.shortcuts import render, redirect
from .models import User, UserForm
import os

def login(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form['user'].data
        password = form['password'].data
        print("Validando usuario")
        print(user)
        print(password)

        result = User.objects.filter(user=user, password=password)

        if result and len(result) == 1:
            request.session['user'] = user
            return redirect('recommendations')
        else:
            return render(request, "login/login.html", context={'form': form})
    else:
        return render(request, "login/login.html", context={'form': form})


def register(request):
    print("Creando usuario")
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = User()
        user.user = form['user'].data
        user.password = form['password'].data

        User.save(user)
        request.session['user'] = user.user
        return redirect('recommendations')
    else:
        return render(request, 'login/create.html', context={'form': form})


def recommendations(request):
    user = request.session['user']
    os.system(f'python ../../src/filtrado_colaborativo.py -u {user}')