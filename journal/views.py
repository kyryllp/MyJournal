from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
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
    posts = Post.objects.all()

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def home_view(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = get_user(request)
        post.save()
        return redirect('/')

    posts = Post.objects.filter(author=get_user(request))

    context = {
        'form': form,
        'posts': posts,
        'user': get_user(request)
    }

    return render(request, 'home.html', context)


def edit_view(request, key):
    post = get_object_or_404(Post, id=key)
    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = get_user(request)
        post.save()

        return redirect('/')

    return render(request, 'edit.html', {'form': form})


def delete_view(request, key):
    post = get_object_or_404(Post, id=key)
    post.delete()

    return redirect('/')
