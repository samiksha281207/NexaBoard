from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout


def register(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            render(request, 'register.html', {
                'error': 'Username already exists. Please choose another username.'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('register')
    return render(request, 'register.html')
def user_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')
def user_logout(request):
    logout(request)
    return redirect('/')

# Create your views here.
