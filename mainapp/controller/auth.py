from django.shortcuts import render, redirect
from mainapp.decorators import redirect_authenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from mainapp.models import Profile
from mainapp.forms import RegisterForm, ProfileForm


@redirect_authenticated_user
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '建立帳號成功')
            return redirect('login2')
    return render(request, 'store/auth/register.html', locals())


@redirect_authenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, '歡迎登入 ! !')
                return redirect('home')
            else:
                messages.error(request, '帳號尚未啟用 ! !')
        else:
            messages.error(request, '帳號或密碼輸入錯誤 ! !')

    return render(request, 'store/auth/login.html', locals())


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, '已登出')
        return redirect('home')


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'store/auth/profile.html', locals())


@login_required
def profile_setting(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, '個人資料修改成功 ! !')
            return redirect('profile')

    return render(request, 'store/auth/profile_setting.html', locals())
