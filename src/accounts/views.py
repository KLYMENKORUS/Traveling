from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegistrationForm


__all__ = (
    'login_user',
    'logout_user',
    'registration'
)


def login_user(request):
    form = UserLoginForm()
    _next = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            _next = _next or 'home'
            messages.success(request, f'Вы успешно выполнили вход с логином: {username}')
            return redirect(_next)
    return render(request, 'accounts/login_form.html', {'form': form})


@login_required()
def logout_user(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли с аккаунта')
    return redirect('home')


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.save()
            messages.success(request, 'Пользователь с логином '
                                      f'{new_user.username} успешно создан')
            return redirect('accounts:login')
        return render(request, 'accounts/registration.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'accounts/registration.html', {'form': form})

