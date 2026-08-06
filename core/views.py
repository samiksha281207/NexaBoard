from django.shortcuts import render
def home(request):
    return render(request, 'home.html')
def projects(request):
    return render(request, 'projects.html')
def add_project(request):
    return render(request, 'add_project.html')
# Create your views here.
