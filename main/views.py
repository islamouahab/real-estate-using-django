from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render , redirect
from django.contrib.auth import login , authenticate , logout 
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def home(request):
   if not request.user.is_authenticated:
      return render(request , 'home.html',{'auth':False})
   else:
      return render(request , 'home.html',{'auth':True})

def login_view(request):
   if not request.user.is_authenticated:
     return render(request , 'login.html')
   else:
      return HttpResponseRedirect(reverse("home"))
def login_handle(request):
    wrong_creds = "your username or password is incorrect"
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request ,username = username , password = password)
        if user is not None:
           login(request , user)
        else:
           return render(request , 'login.html', {'error_message':wrong_creds})
    return HttpResponseRedirect(reverse("login"))
def create_user(request):
   if request.method=='POST':
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']
      if not username or not email or not password:
         messages.error(request , 'All fields must be filled')
         return redirect('create_user')
      user = User.objects.create_user(username=username , email=email , password=password)
      return HttpResponseRedirect(reverse('login'))
   else:
      return render(request , 'signup.html')
def logout_handle(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))