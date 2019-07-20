from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *


# Create your views here.
def login_view(request):
    next_ = request.GET.get('next')
    form = LoginUserForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)

        if next_:
            return redirect(next_)
        return redirect('/')
    return render(request, 'login.html', {'form': form})


def register_view(request):
    next_ = request.GET.get('next')
    form = RegisterUserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next_:
            return redirect(next_)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def home_view(request):
    form = CreatePostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = get_user(request)
        post.save()

    return render(request, 'home.html', {'form': form})
