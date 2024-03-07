from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import login , authenticate , logout
# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
     return render(request , 'login.html')
    return render(request , 'home.html')
def login_handle(request):
    wrong_creds = "your username or password is incorrect"
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request ,username = username , password = password)
        if user is not None:
           login(request , user)
           return HttpResponseRedirect(reverse("login"))
        else:
           return render(request , 'login.html', {'error_message':wrong_creds})
def logout_handle(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))