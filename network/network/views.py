import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from django.core.paginator import Paginator
from .models import User, posts, UserProfiles


def index(request):
    user_posts = posts.objects.all().order_by('-created_at')
    
    # List of all likes for each post (based on 'user_posts')
    likes_usernames = []
    for userpost in user_posts:
        likes_usernames.append(list(userpost.likes.values_list('username', flat=True)))
    
    # List of all post (based on 'user_posts')
    post_list = list(user_posts.values('id', 'username__username', 'post', 'created_at'))
    
    for post, likes_usernames in zip(post_list, likes_usernames):
        post['username'] = post.pop('username__username')
        post['like_status'] = False 
        post['likes_usernames'] = likes_usernames
        post['total_likes'] = len(likes_usernames)
        
        print(post['likes_usernames'])
        
        if request.user.username in post["likes_usernames"]:
            post['like_status'] = True
        print(request.user.username, '-' ,post['like_status'])
    
    # print(post_list)
    
    # Pagination
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj,
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
            
            # create UserProfiles for follow/following
            UserProfiles.objects.create(user=user)
            
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def post(request):
    if request.method == "POST":
        post = request.POST.get("new_post")
        
        if post:
            try:
                post_save = posts.objects.create(username=request.user, post=post)
                post_save.save() 
                
            except IntegrityError as debug:
                print(debug)
                return render(request, "network/index.html", {
                    "message": "An exception error occured."
                })
        
        else:
            messages.error(request, "You have not written anything yet.", extra_tags='danger')

        return HttpResponseRedirect(reverse("index"))
    
@csrf_exempt
@login_required
def update_post(request, post_id):
    if request.method == "PUT":
        update_post = json.loads(request.body)
        edited_post_value = update_post['post']

        # To sanitize, prevent unwanted whitespaces
        cleaned_post_value = ' '.join(edited_post_value.split())
        
        try:
            get_post_db = posts.objects.get(pk=post_id)
            get_post_db.post = cleaned_post_value
            get_post_db.save()
            
        except IntegrityError as debug:
            print(debug)
            
        return HttpResponse(status=204)

@csrf_exempt
@login_required
def post_like(request, post_like_id):
    if request.method == "PUT":

        update_like = json.loads(request.body)
        update_like_value = update_like['user_like']
  
        like_post = posts.objects.get(pk=post_like_id)
        likes_user_list = like_post.likes.all()
        
        if update_like_value == True:
            like_post.likes.add(request.user)
        else:
            like_post.likes.remove(request.user)
            
        return HttpResponse(status=204)          
        
def profiles(request, username):
    if request.method == "GET":
        user = get_object_or_404(User, username=username)
        user_posts = posts.objects.filter(username=user).order_by('-created_at')
        
        follower = UserProfiles.objects.get(user=user)
        follower_usernames = [follower.username for follower in follower.followers.all()]
        
        following_status = False
        
        # Not following = False ; Following = True
        if request.user.username in follower_usernames:
            following_status = True
        else:
            following_status = False
            
        # Followers count
        followers_count = follower.followers.count()
        
        # Following count
        following = UserProfiles.objects.filter(followers=user)
        following_count = following.count()
        
        # List of all likes for each post (based on 'user_posts')
        likes_usernames = []
        for userpost in user_posts:
            likes_usernames.append(list(userpost.likes.values_list('username', flat=True)))
       
        # List of all post (based on 'user_posts')
        post_list = list(user_posts.values('id', 'username__username', 'post', 'created_at'))
        
        for post, likes_usernames in zip(post_list, likes_usernames):
            post['username'] = post.pop('username__username')
            post['like_status'] = False 
            post['likes_usernames'] = likes_usernames
            post['total_likes'] = len(likes_usernames)
        
        print(post_list)   
            # print(post['likes_usernames'])
            
        if request.user.username in post["likes_usernames"]:
            post['like_status'] = True
    
    return render(request, "network/profile.html", {
        "username": user,
        "user_posts": user_posts,
        "following_status": following_status,
        "followers_count": followers_count, 
        "following_count": following_count,
        "post_list": post_list,
        
    })

@login_required 
def follow(request, username):
    if request.method == "POST":
        follow_user = request.POST.get("follow")
        unfollow_user = request.POST.get("unfollow")
        
        user = get_object_or_404(User, username=username)
        follow_num = UserProfiles.objects.get(user=user)
        
        if follow_user:
            follow_num.followers.add(request.user)
        
        elif unfollow_user:
            follow_num.followers.remove(request.user)
        
    return HttpResponseRedirect(reverse("profiles", args=[username]))

@login_required
def following(request):
    if request.method == "GET":
        following = UserProfiles.objects.filter(followers=request.user)
        print(following)
        
        following_ids = following.values_list('user', flat=True)
        
        following_post = posts.objects.filter(username_id__in=following_ids).order_by('-created_at')
        
        # List of all likes for each post (based on 'user_posts')
        likes_usernames = []
        for userpost in following_post:
            likes_usernames.append(list(userpost.likes.values_list('username', flat=True)))
       
        # List of all post (based on 'user_posts')
        post_list = list(following_post.values('id', 'username__username', 'post', 'created_at'))
        
        for post, likes_usernames in zip(post_list, likes_usernames):
            post['username'] = post.pop('username__username')
            post['like_status'] = False 
            post['likes_usernames'] = likes_usernames
            post['total_likes'] = len(likes_usernames)

            if request.user.username in post["likes_usernames"]:
                post['like_status'] = True
            
        return render(request, "network/following.html", {
            "post_list": post_list,
        })