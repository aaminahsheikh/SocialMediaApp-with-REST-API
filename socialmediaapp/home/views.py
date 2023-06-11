from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import CreatePost, User
from . forms import CreatePostForm, UserRegistrationForm


# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            print('Not found!') 
        print(email, password)

        user = authenticate(request, email=email, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect('home')
        else:
            print(user)
        
    context = {}
    return render(request, 'home/login_register.html', context)

def user_logout(request):
    logout(request)

    return redirect("login")

def user_register(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    page = 'register'
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Before saving the user, get its IP & save into DB.
            get_ip = request.META.get('HTTP_X_FORWARDED_FOR')

            if get_ip:
                ipaddress = get_ip.split(',')[-1].stripe()
            else:
                ipaddress = request.META.get('REMOTE_ADDR')
            
            user.ip = ipaddress
            user.save()

            user = authenticate(request, email=user.email, 
                password=request.POST['password1'])

            if user:
                login(request, user)
                return redirect("home")

    context = {'form': form, 'page': page}
    return render(request, 'home/login_register.html', context)

def home(request):
    posts = CreatePost.objects.all()
    context = {'posts': posts}
    return render(request, 'home/home.html', context)

@login_required(login_url="login")
def create_post(request):
    form = CreatePostForm()

    if request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)

            form.post_user = request.user
            form.save()

            return redirect('home')

    context = {'form': form}
    return render(request, 'home/create_post.html', context)

@login_required(login_url="login")
def update_post(request, pk):
    post = CreatePost.objects.get(id=pk)
    form = CreatePostForm(instance=post)

    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'home/create_post.html', context)


@login_required(login_url="login")
def delete_post(request, pk):
    post = CreatePost.objects.get(id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
    context = {}
    return render(request, 'home/delete_post.html', context)

@login_required(login_url="login")
def like_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(CreatePost, id=pk)
        
        if post.post_likes.filter(id=request.user.id):
            post.post_likes.remove(request.user)
        
        else:
            post.post_likes.add(request.user)

        return redirect("home")
    