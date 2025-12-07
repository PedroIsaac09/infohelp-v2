from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm


class CustomLoginView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("inicio")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def home(request):
    return render(request, "infohelp/templates/inicio.html")
