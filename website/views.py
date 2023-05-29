import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import Max
from django.forms import modelformset_factory
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, View

from .models import Listing, Comment, Image, Contact, Profile
from .forms import listingForm, listingGetRequestForm, UserUpdateForm, ProfileUpdateForm


# Create your own mixins
class StaffMemberRequiredMixin(object):
    @method_decorator(staff_member_required)
    def as_view(self, *args, **kwargs):
        return super(StaffMemberRequiredMixin, self).as_view(*args, **kwargs)


# Create your views here.
def index (request):
    agents = User.objects.filter(is_staff=True, is_active=True)
    posts = Listing.objects.filter(active=True).order_by("-time_created")[0:10]
    listing_form = listingGetRequestForm()
    return render(request, 'website/index.html', {
        'agents': agents,
        'listing_form': listing_form,
        'posts': posts
    })


class PropertiesListView (ListView):
    model = Listing
    queryset = Listing.objects.filter(active=True).order_by("-time_created").all()
    paginate_by = 25 # show 25 posts in reverse chronologial order
    template_name = "website/properties.html"

    def get_context_data (self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = listingGetRequestForm()
        return context


def single_property (request, item):
    try:
        post = Listing.objects.get(id=item)
    except Listing.DoesNotExist:
        post = ""
    return render(request, 'website/singleProperty.html', {
        'post': post
    })


class FilteredPropertiesListView (ListView):
    model = Listing
    paginate_by = 25 # show 25 posts in reverse chronologial order
    template_name = "website/properties.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.filter(
                category=self.request.GET['category'],
                purpose=self.request.GET['purpose'],
                active=True
            ).order_by("-time_created").all()
        # SEARCH BY LOCATION
        if self.request.GET['location']:
            qs = qs.filter(
                address__icontains=self.request.GET['location']
            )

        # SEARCH BY CITY
        if self.request.GET['city'] != '':
            qs = qs.filter(
                city=self.request.GET['city']
            )

        # SEARCH BY PRICE RANGE
        if self.request.GET['min_price'] and self.request.GET['max_price']:
            qs = qs.filter(
                price__range=(self.request.GET['min_price'], self.request.GET['max_price'])
            )
        elif self.request.GET['min_price']:
            max_price = qs.aggregate(
                Max('price')
            )['price__max']
            qs = qs.filter(
                price__range=(self.request.GET['min_price'], max_price)
            )
        elif self.request.GET['max_price']:
            qs = qs.filter(
                price__range=(0, self.request.GET['max_price'])
            )
        
        # SEARCH BY AREA SIZE
        if self.request.GET['area_size']:
            qs = qs.filter(
                area_size=self.request.GET['area_size'],
                area_size_unit=self.request.GET['area_size_unit']
            )
        return qs
        
    def get_context_data (self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = listingGetRequestForm()
        return context


class CategoryListView (ListView):
    model = Listing
    paginate_by = 25 # show 25 posts in reverse chronologial order
    template_name = "website/properties.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)

        if self.kwargs['type'] == 'Homes':
            subcategories = ['house', 'flat', 'up', 'lp', 'fh', 'room', 'ph']
        elif self.kwargs['type'] == 'Plots':
            subcategories = ['rp', 'cp', 'al', 'il', 'pfile', 'pform']
        elif self.kwargs['type'] == 'Commercial':
            subcategories = ['off', 'shop', 'wh', 'fact', 'buil']

        qs = qs.filter(
            category__in=subcategories,
            active=True
        ).order_by('-time_created').all()
        return qs
        
    def get_context_data (self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = listingGetRequestForm()
        return context


@csrf_exempt
def contact (request):
    # Composing a new message must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check sender email
    data = json.loads(request.body)

    # Get contents of contact
    fname = data.get("fname", "")
    lname = data.get("lname", "")
    phone_number = data.get("phone_number", "")
    email = data.get('email', '')
    message = data.get("message", "")

    if fname == "":
        return JsonResponse({
            "error": "First Name is required."
        }, status=400)

    if phone_number == "":
        return JsonResponse({
            "error": "Phone number is required."
        }, status=400)

    if email == "":
        return JsonResponse({
            "error": "Email is required."
        }, status=400)

    if message == "":
        return JsonResponse({
            "error": "Message is required."
        })
        
    # Create contact
    contact = Contact(
        fname = fname,
        lname = lname,
        phone_number = phone_number,
        email = email,
        message = message
    )
    contact.save()
    return JsonResponse({"message": "Thankyou for contacting us."}, status=201)


def about_us (request):
    return render(request, 'website/about-us.html')


def contact_us_page (request):
    if request.user.is_staff and request.user.is_authenticated:
        contacts = Contact.objects.all()
        contacts = contacts.order_by("-date_created").all()
        return render(request, 'website/contactUs.html', {
            'contacts': contacts
        })
    return render(request, 'website/contactUs.html')


def agents (request):
    agents = User.objects.all()
    return render(request, 'website/agents.html', {
        'agents': agents
    })


class profileWithPropertiesListView(ListView, LoginRequiredMixin):
    model = Listing
    paginate_by = 25 # show 25 posts in reverse chronologial order
    template_name = "website/profile.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.filter(
                creator=self.request.user,
                active=True
            ).order_by("-time_created").all()
        return qs


@login_required
def profileUpdate (request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'website/profile-update.html',{
        'u_form': u_form,
        'p_form': p_form
    })


@login_required
def createListing (request):

    if request.method == "POST":
        listing_form = listingForm (request.POST)
        images = request.FILES.getlist('images')
        bedroom = request.POST['bedroom']
        bathroom = request.POST.get('bathroom', None)
        category_list = ['house', 'flat', 'up', 'lp', 'fh', 'room', 'ph']

        if listing_form.is_valid():
            listing_obj = listing_form.save(commit=False)
            listing_obj.creator = request.user
            listing_obj.purpose = request.POST['purpose']

            if listing_obj.category in category_list:
                if listing_obj.custom_bdroom:
                    listing_obj.bedroom = ''
                elif bedroom:
                    listing_obj.bedroom = bedroom

                if (bedroom or listing_obj.custom_bdroom) and listing_obj.custom_bthroom:
                    listing_obj.bathroom = ''
                elif (bedroom or listing_obj.custom_bdroom) and bathroom:
                    listing_obj.bathroom = bathroom
            else:
                listing_obj.bedroom = ''
                listing_obj.bathroom = ''
            listing_obj.active = True
            listing_obj.save()

            for image_file in images:
                img = Image(listing=listing_obj, image=image_file)
                img.save()

            messages.success(request, "Yeew, check it out on the home page!")
            return HttpResponseRedirect("/createListing")
        
        else:
            for field in listing_form:
                for error in field.errors:
                    messages.error(request, f"{field.name}: {error}")
            print(listing_form.errors)
            return render(request, 'website/createListing.html', {
                'listing_form': listing_form,
            })

    listing_form = listingForm
    return render(request, 'website/createListing.html', {
        'listing_form': listing_form,
    })
        
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is None:
            return render(request, "website/login.html", {
                "error_message": "Invalid username and/or password."
            })
        else:
            login(request, user)
            return redirect("index")
    else:
        return render(request, "website/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone_number = request.POST["tel"]
        estate_name = request.POST["estate_name"]
        bio_info = request.POST["bio_info"]
        profile_image = request.FILES.get("profile_image")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "website/register.html", {
                "pass_error_message": "Passwords must match.",
                'pass_error': True
            })
        elif password in username:
            return render(request, "website/register.html", {
                "pass_error_message": "Your password can't be similar to username.",
                'pass_error': True
            })
        elif password in email:
            return render(request, "website/register.html", {
                "pass_error_message": "Your password can't be similar to email.",
                'pass_error': True
            })


        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name = first_name, last_name = last_name)
            user.save()
            profile = Profile(user=user)
            profile.bio_info = bio_info
            profile.estate_name = estate_name
            profile.phone_number = phone_number
            if profile_image:
                profile.profile_image = profile_image
            profile.save()
        except IntegrityError:
            return render(request, "website/register.html", {
                "username_error_message": "Username already taken.",
                'username_error': True
            })
        messages.success(request, "Hurray! Your account has been activated.")
        login(request, user)
        return redirect("index")
    else:
        return render(request, "website/register.html")