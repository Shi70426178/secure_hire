from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def login_choice(request):
    return render(request, "login_choice.html")

def signup_choice(request):
    return render(request, "signup_choice.html")

