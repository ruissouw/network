from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Post


def index(request):
    posts = Post.objects.all()
    return render(request, "network/index.html", {"posts": posts})


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


def post(request):
    # Redirect user to index if request not via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Ensure there is some text in the post
    content = request.POST.get("content", "").strip()
    if not content:
        messages.error(request, "Post must contain some text!")
        return redirect("index")

    # Create and save the post
    user = request.user
    post = Post(content=content, user=user)
    post.save()
    return redirect("index")


def profile(request, user_id):
    current_user = request.user
    try:
        profile_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error":"User does not exist"}, status=400)
    is_following = profile_user.followers.filter(id=current_user.id).exists()
    return render(request, "network/profile.html", {
        "profile_user":profile_user,
        "current_user":current_user,
        "is_following":is_following
    })

@csrf_exempt
def follow(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        user_id = data.get('user_id')

        # Assuming you have a User model and a relationship for followers
        user_to_follow = User.objects.get(id=user_id)
        current_user = request.user

        if user_to_follow in current_user.following.all():
            current_user.following.remove(user_to_follow)
            following = False
        else:
            current_user.following.add(user_to_follow)
            following = True

        return JsonResponse({'following': following})

    elif request.method == "GET":
        return JsonResponse({'error': 'Invalid request'}, status=400)

def edit(request):
    pass