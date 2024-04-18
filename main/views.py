from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render , redirect
from django.contrib.auth import login , authenticate , logout 
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import custom_user,post,media_files
# Create your views here.
def home(request):
   posts = post.objects.prefetch_related('media_files_set').all()
   if not request.user.is_authenticated:
      return render(request , 'home.html',{'auth':False ,'delete_alert':False , 'posts':posts})
   else:
      return render(request , 'home.html',{'auth':True , 'posts':posts})

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
def profile(request , user_id):
   if request.user.id==user_id :
      return render(request , 'profile.html',{'alert':False})
   else:
      raise PermissionDenied()

def create_user(request):
   if request.method=='POST':
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']
      phone_num = request.POST['phone_num']
      if not username or not email or not password:
         messages.error(request , 'All fields must be filled')
         return redirect('create_user')
      user = custom_user.objects.create_user(username=username , email=email , password=password , phone_num=phone_num)
      return HttpResponseRedirect(reverse('login'))
   else:
      return render(request , 'signup.html')
def delete_user(request,user_id):
    user = custom_user.objects.get(pk=user_id)
    logout(request)
    user.delete()
    return render(request , 'home.html',{'auth':False , 'delete_alert':True})
def update_profile(request , user_id):
   if request.method == 'POST':
      username = request.POST['username']
      phone_num = request.POST['phone_num']
      user = custom_user.objects.get(pk=user_id)
      user.username = username
      user.phone_num = phone_num
      if request.FILES:
        profile_pic = request.FILES['profile_pic']
        user.profile_pic = profile_pic
      user.save()
      alert = True
      return render(request , 'profile.html',{'alert':True})
def logout_handle(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))