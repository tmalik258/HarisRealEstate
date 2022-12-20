from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import listing, User, Category, Comments, Images
from .forms import listingForm, imageForm
from django.forms import modelformset_factory
from django.contrib import messages


# Create your views here.
def index (request):
    agents = User.objects.all()
    return render(request, 'website/index.html', {
        'agents': agents
    })

@login_required
def profile (request):
    try:
        posts = listing.objects.get(creator=request.user)
    except listing.DoesNotExist:
        posts = "Empty!! No listing found"
    return render(request, 'website/profile.html',{
        'posts': posts
    })

@login_required
def createListing (request):
    ImageFormSet = modelformset_factory(Images, form=imageForm, extra=5)
     #'extra' means the number of photos that you can upload

    if request.method == "POST":
        listing_form = listingForm (request.POST)
        image_form = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

        if listing_form.is_valid() and image_form.is_valid():
            listingform = listing_form.save(commit=False)
            listingform.user = request.user
            listingform.active = True
            listingform.save()

            for form in image_form.cleaned_data:
                #this helps to not crash if the user do not upload all the photos
                if form:
                    image = form['images']
                    photo = Images(listing=listingform, image=image)
                    photo.save()

            # use django messages framework
            messages.success(request, "Yeew, check it out on the home page!")
            return HttpResponseRedirect("/createListing")
        
        else:
            print(listingForm.errors, image_form.errors)

    else:
        listing_form = listingForm
        image_form = ImageFormSet(queryset=Images.objects.none())

    return render(request, 'website/createListing.html', {
        'listing_form': listing_form,
        'image_form': image_form
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
            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, "website/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "website/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        bio_info = request.POST["bio_info"]
        profile_image = request.POST["profile_image"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "website/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if profile_image:
                user = User.objects.create_user(username, email, password, first_name = first_name, last_name = last_name, bio_info = bio_info, profile_image = profile_image)
            else:
                user = User.objects.create_user(username, email, password, first_name = first_name, last_name = last_name, bio_info = bio_info)
            user.save()
        except IntegrityError:
            return render(request, "website/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("profile"))
    else:
        return render(request, "website/register.html")