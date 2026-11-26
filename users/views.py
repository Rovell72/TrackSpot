from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Аккаунт создан! Добро пожаловать.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Профиль обновлён.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        try:
            user = User.objects.get(email__iexact=email)
            request.session['reset_user_id'] = user.id
            return redirect('password_reset_set')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не найден.')
    return render(request, 'users/password_reset.html')


def password_reset_set(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('password_reset')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.pop('reset_user_id', None)
        return redirect('password_reset')

    if request.method == 'POST':
        pwd1 = request.POST.get('password1', '')
        pwd2 = request.POST.get('password2', '')
        if pwd1 and pwd1 == pwd2:
            user.set_password(pwd1)
            user.save()
            request.session.pop('reset_user_id', None)
            messages.success(request, 'Пароль изменён. Войдите с новым паролем.')
            return redirect('login')
        messages.error(request, 'Пароли не совпадают или пустые.')

    return render(request, 'users/password_reset_set.html', {'reset_user': user})
