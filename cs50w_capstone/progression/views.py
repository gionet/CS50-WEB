from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import User, Posts
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta, date, time

import json
import csv

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        username = request.user.username

        user_posts = Posts.objects.filter(username=request.user).order_by('created_at')
        user_post_dict = {}
        
        for user_post in user_posts:
            if user_post.timeline not in user_post_dict:
                user_post_dict[user_post.timeline] = []
            
            user_post_dict[user_post.timeline].append(user_post.post)
            
        user_post_dict_json = json.dumps(user_post_dict)
        # print(user_post_dict)
        
        return render(request, "progression/homepage.html", {
            "username": username,
            "user_post_dict": user_post_dict,
        })
    
    else:
        return render(request, "progression/homepage.html")
       
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
            # return render(request, "progression/homepage.html", {
            #     "username": username
            # })
        else:
            return render(request, "progression/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "progression/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "progression/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print("error:", e)
            return render(request, "progression/register.html", {
                "message": e #"Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "progression/register.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def create_post(request):
    if request.method == "POST":
        try:
            create_post = json.loads(request.body)
            print(create_post)
            timeline = create_post["timeline"]
            post = create_post["post"]
            print(timeline)
            print(post)
        
            save_post = Posts.objects.create(username=request.user, post=post, timeline=timeline)
            save_post.save()
            
            return JsonResponse({"message": "Post created"}, status=204, safe=False)
    
        except Exception as e:
            print("Exception:", e)
            return JsonResponse({"error": str(e)}, status=500)
        
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def delete_post(request):
    if request.method == "DELETE":
        try:
            delete_post = json.loads(request.body)
            print(delete_post)
            
            timeline = delete_post["timeline"]
            post = delete_post["post"]
            print(timeline)
            print(post)
            
            del_post = Posts.objects.filter(username=request.user, timeline=timeline, post=post).delete()

            return JsonResponse({"message": "Post deleted"}, status=204)

        except Exception as e:
            print("Exception:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def update_post(request):
    if request.method == "PUT":
        try:
            update_post = json.loads(request.body)
            print(update_post)
            
            post = update_post["post"]
            completion = update_post["completion"]
            timeline = update_post["timeline"]
            
            # Update 'updated_at' instance manually due to being Update and not Save
            update_at = Posts.objects.filter(username=request.user, timeline=timeline, post=post).first()
            if update_at:
                update_at.completion = completion
                update_at.updated_at = timezone.now()
                update_at.save()
                
            return JsonResponse({"message": "Post updated successfully"})
            
        except Exception as e:
            print("Exception:", e)
            return JsonResponse({"error": str(e)}, status=500)
            
    return HttpResponseRedirect(reverse("index"))
    
@login_required
def timeFrame(request, timeFrame):
    current_year = timezone.now().year
    current_month = timezone.now().month
    
    # Post that are in-progress (without considering Time Frames)
    user_posts = Posts.objects.filter(
        username=request.user.id, 
        timeline=timeFrame, 
        completion=False,
        ).order_by('updated_at')
    
    user_post_dict = {}
    
    # for user_post in user_posts:
    #     if user_post.timeline not in user_post_dict:
    #         user_post_dict[user_post.timeline] = []
        
    #     user_post_dict[user_post.timeline].append(user_post.post)
    
    # Post that exceeds 24 hours since the last modification
    posts_completes_24hrs = Posts.objects.filter(
        username=request.user.id,
        timeline=timeFrame, 
        completion=True,
        updated_at__lt =timezone.now() - timedelta(hours=24)
        ).order_by('updated_at')

    user_post_dict['completed_more_than_24h'] = []
    for post_completes_24hr in posts_completes_24hrs:
        user_post_dict['completed_more_than_24h'].append(post_completes_24hr.post)
    
    if timeFrame == 'yearly':
        start_datetime_prev = timezone.make_aware(datetime(year=current_year-1, month=1, day=1))
        end_datetime_prev = timezone.make_aware(datetime(year=current_year, month=1, day=1))
        
        start_datetime_current = timezone.make_aware(datetime(year=current_year, month=1, day=1))
        end_datetime_current = timezone.make_aware(datetime(year=current_year + 1, month=1, day=1))
        
    elif timeFrame == 'monthly':
        start_datetime_prev = timezone.make_aware(datetime(year=current_year, month=current_month-1, day=1))
        end_datetime_prev = timezone.make_aware(datetime(year=current_year, month=current_month, day=1))
        
        start_datetime_current = timezone.make_aware(datetime(year=current_year, month=current_month, day=1))
        end_datetime_current = timezone.make_aware(datetime(year=current_year, month=current_month + 1, day=1))
    
    elif timeFrame == 'weekly':
        totalDaysWeek = timedelta(days=7)
        start_datetime_prev = timezone.now() - timedelta(timezone.now().weekday()) - totalDaysWeek
        end_datetime_prev = timezone.now() - timedelta(timezone.now().weekday())
        
        start_datetime_current = timezone.now() - timedelta(timezone.now().weekday())
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        end_datetime_current = start_datetime_current + totalDaysWeek
    
    else: # if timeFrame == ‘daily’
        print(datetime.today())
        start_datetime_prev = datetime.today() - timedelta(days=1)
        end_datetime_prev = start_datetime_prev + timedelta(days=1)
        
        start_datetime_current = timezone.now()
        end_datetime_current = datetime.today() + timedelta(days=1)
    
    # Previous year/month/week/day
    start_datetime_prev = start_datetime_prev.replace(hour=0, minute=0, second=0, microsecond=0)
    end_datetime_prev = end_datetime_prev.replace(hour=0, minute=0, second=0, microsecond=0)
    print(f'Start previous ({timeFrame}):', start_datetime_prev)
    print(f'End previous ({timeFrame}):', end_datetime_prev)
    
    posts_incompletes = Posts.objects.filter(
        username=request.user.id,
        timeline=timeFrame,
        completion=False,
        updated_at__range=(start_datetime_prev, end_datetime_prev)
    ).order_by('updated_at')
    
    user_post_dict['incomplete'] = []
    for posts_incomplete in posts_incompletes:
        user_post_dict['incomplete'].append(posts_incomplete.post)
    
    # Putting start datetime and end datetime in
    user_post_dict['start_to_end'] = [start_datetime_prev.strftime('%Y-%m-%d') + " to " + end_datetime_prev.strftime('%Y-%m-%d')]
    
    # Current year/month/week/day
    start_datetime_current = start_datetime_current.replace(hour=0, minute=0, second=0, microsecond=0)
    end_datetime_current = end_datetime_current.replace(hour=0, minute=0, second=0, microsecond=0)
    print(f'Start current ({timeFrame}):', start_datetime_current)
    print(f'End current ({timeFrame}):', end_datetime_current)
    
    posts_incompletes = Posts.objects.filter(
        username=request.user.id,
        timeline=timeFrame,
        completion=False,
        updated_at__range=(start_datetime_current, end_datetime_current)
    ).order_by('updated_at')
            
    user_post_dict[timeFrame] = []
    for posts_incomplete in posts_incompletes:
        user_post_dict[timeFrame].append(posts_incomplete.post)
    
    # Post that is within respective TimeFrame since the last modification
    twentyfour_hour_ago = timezone.now() - timedelta(hours=24)
    posts_completes = Posts.objects.filter(
        username=request.user.id, 
        timeline=timeFrame, 
        completion=True,
        updated_at__range = [start_datetime_current, end_datetime_current],
        ).order_by('updated_at')
    
    user_post_dict['completed'] = []
    for posts_complete in posts_completes:
        user_post_dict['completed'].append(posts_complete.post)
    
    print(user_post_dict)
    
    try:
        # values_only = list(user_post_dict.values())[0]
        # print(values_only)
        return JsonResponse(user_post_dict, safe=False)
    
    except Exception as e:
        print("Exception:", e)
        return JsonResponse({"error": str(e)}, status=500)

def generate_csv(request): # Generate CSS file
    # Query data from database
    queryset = Posts.objects.filter(
        username=request.user.id,
        ) # Query all objects from model
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
   
    # Write data to CSV
    writer = csv.writer(response)
    
    # Define the header row
    header_row = ['No.', 'Post', 'Timeline', 'Created_at', 'Updated_at', 'Completion']
    
    # Write the header row to the CSV file
    writer.writerow(header_row)
    
    # Initialize a counter
    counter = 1
    
    # Write header row
    for obj in queryset:
        writer.writerow([counter, obj.post, obj.timeline, obj.created_at, obj.updated_at, obj.completion])

        counter += 1
        
    return response