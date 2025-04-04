from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render , redirect
from django.contrib.auth import login , authenticate , logout 
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import custom_user,post,media_files
from algerography.models import Wilaya
# Create your views here.
def home(request):
   posts = post.objects.prefetch_related('media_files_set').all()
   wilayas = Wilaya.objects.all()
   max_length = 120
   description  = [post.description[:max_length]+ '...' if len(post.description)>max_length else post.description for post in posts]
   if not request.user.is_authenticated:
      return render(request , 'home.html',{'auth':False ,'delete_alert':False ,'wilayas':wilayas, 'posts':zip(posts,description)})
   else:
      return render(request , 'home.html',{'auth':True ,'wilayas':wilayas, 'posts':zip(posts,description)})

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
   if request.user.is_authenticated:
      if request.user.id != user_id:
         User = custom_user.objects.get(pk=user_id)
         owner = False
      else:
         User = None
         owner = True
      Posts = post.objects.prefetch_related('media_files_set').filter(user_id=user_id)
      max_length = 120
      description  = [post.description[:max_length]+ '...' if len(post.description)>max_length else post.description for post in Posts]
      return render(request , 'profile.html',{'alert':False,'owner':owner,'User':User,'posts':zip(Posts,description)})
   else:
      return HttpResponseRedirect(reverse('login'))
  

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
def add_post(request):
    if request.method=='POST':
       title = request.POST['title']
       space = request.POST['area']
       floor = request.POST['floor']
       price = request.POST['price']
       description = request.POST['description']
       location = request.POST['location']
       Post = post(user_id=request.user , title=title , space=space, floor_num=floor, price=price , description=description , location=location)
       Post.save()
       if 'media' in request.FILES:
        for file in request.FILES.getlist('media'):
          media = media_files(post_id=Post , path=file)
          media.save()
       return HttpResponseRedirect(reverse('home'))
    return render(request , 'add post.html')
    
def show_post(request,post_id):
   Post = post.objects.prefetch_related('media_files_set').get(pk=post_id)
   return render(request,'post.html',{'post':Post,'auth':request.user.is_authenticated ,'wilayas':Wilaya.objects.all()})
def update_post(request,post_id):
   Post = post.objects.prefetch_related('media_files_set').get(pk=post_id)
   if request.user == Post.user_id:
    if request.method=='POST':
       Post.title = request.POST['title']
       Post.space = request.POST['area']
       Post.floor_num = request.POST['floor']
       Post.price = request.POST['price']
       Post.description = request.POST['description']
       Post.location = request.POST['location']
       Post.save()
       if 'media' in request.FILES:
        if request.FILES:
         for file in Post.media_files_set.all():
          file.delete()
         for file in request.FILES.getlist('media'):
          media = media_files(post_id=Post , path=file)
          media.save()
       return HttpResponseRedirect(reverse('home'))
    return render(request,'post update.html',{'post':Post}) 
   else:
      raise PermissionDenied()
def delete_post(request,post_id):
    Post = post.objects.prefetch_related('media_files_set').get(pk=post_id)
    for file in Post.media_files_set.all():
       file.delete()
    Post.delete()
    
    return HttpResponseRedirect(reverse('home'))
def delete_user(request,user_id):
    user = custom_user.objects.get(pk=user_id)
    Post = post.objects.filter(user_id=user)
    Post.delete()
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
      return HttpResponseRedirect(reverse('profile', args=(request.user.id,)))
def safe_casting(value):
  try:
     return int(value)
  except:
    return None
def search(request):
   query = Q()
   search_key = request.POST['search']
   location = request.POST['location'] or None
   min_price = safe_casting(request.POST['min_price'])
   max_price = safe_casting(request.POST['max_price'])
   min_space = safe_casting(request.POST['min_space']) 
   max_space = safe_casting(request.POST['max_space'])
   floor = safe_casting(request.POST['floor'])
   if search_key is not None:
      query &= Q(title__icontains=search_key)
   if location is not None:
      query &= Q(location__icontains=location)
   if max_price is not None:
      query &= Q(price__lt=max_price)
   if min_price is not None:
      query &= Q(price__gt=min_price) 
   if max_space is not None:
      query &= Q(space__lt=max_space) 
   if min_space is not None:
      query &= Q(space__gt=min_space) 
   if floor is not None:
      query &= Q(floor_num=floor)
   Posts = post.objects.filter(query)
   max_length = 120
   description  = [post.description[:max_length]+ '...' if len(post.description)>max_length else post.description for post in Posts]
   return render(request,'home.html',{'posts':zip(Posts,description) ,'auth':request.user.is_authenticated ,'wilayas':Wilaya.objects.all()})
def logout_handle(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))