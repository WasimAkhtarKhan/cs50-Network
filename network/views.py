from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect #,get_object_or_404
from django.urls import reverse
from datetime import datetime


from .models import User,Post ,Profile

def create(request):
    if request.method == "POST":
        post = Post()
        post.user = request.user.username
        post.content = request.POST.get('content')
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        post.date = dt
        post.save()

        return redirect('index')

    else:
        return redirect('index')


def viewProfile(request,username):
    if request.method == "GET":
        posts = Post.objects.filter(user=username).order_by('-id')
        #profile = Profile.objects.get(user__username=username)
        followers = Profile.objects.filter(following=username)
        no_of_followers = followers.count()
        followings = Profile.objects.filter(user__username=username)
        no_of_followings = followings.count()
        try:
            profile = Profile.objects.get(user=request.user,following=username)#Already Following
            if(profile):
                AlreadyFollow = True
        except:
            AlreadyFollow = False

        return render(request, 'network/profile.html',{
            'posts':posts,
            'username':username,
            'alreadyFollow':AlreadyFollow,
            'no_of_followers':no_of_followers,
            'no_of_followings':no_of_followings,
        })

def follow(request,username):
    #Create New Profile
    if request.method == "GET":
        profile = Profile.objects.get_or_create(user=request.user,following=username)
        if(profile):
            pass
        else:
            profile.save()

    return HttpResponseRedirect(reverse("index"))


def unfollow(request,username):
    #Create New Profile
    if request.method == "GET":
        profile = Profile.objects.get(user=request.user,following=username)
        if(profile):
            profile.delete()
        else:
            pass

    return HttpResponseRedirect(reverse("index"))
    


def index(request):
    if request.method == "GET":
        posts = Post.objects.all().order_by('-id')
        allpost = True
    return render(request, "network/index.html",{
        "posts":posts,
        "AllPost":allpost,
    })

def viewFollowings(request):
    
    if request.method == "GET":
        totalPosts = []
        profiles = Profile.objects.filter(user__username=request.user.username)
        posts = Post.objects.all().order_by('-id')
        for p in posts:
            for profile in profiles:
                if profile.following == p.user :
                    totalPosts.append(p)

    return render(request, "network/index.html",{
        "totalPosts":totalPosts,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
