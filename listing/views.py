import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import Max
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, View

from .models import Listing, ListingImage, Contact
from .forms import listingForm


# Create your views here.
def index (request):
    posts = Listing.posts.all()[0:10]
    return render(request, 'listing/index.html', {
        'posts': posts
    })


class PropertiesListView (ListView):
    model = Listing
    queryset = Listing.posts.all()
    paginate_by = 25 # show 25 posts in reverse chronologial order
    template_name = "listing/properties.html"


def single_property (request, item):
    active = False

    try:
        post = Listing.objects.get(pk=item)

        if request.user.is_authenticated and request.user.username == post.creator.username:
            active = True

    except Listing.DoesNotExist:
        post = ""
    return render(request, 'listing/singleProperty.html', {
        'post': post,
        'active': active
    })

class SearchedPropertiesListView (ListView):
    model = Listing
    queryset = Listing.posts.all()
    paginate_by = 25 # show 25 posts in reverse chronologial order
    template_name = "listing/properties.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.filter(
                title__icontains=self.request.GET['searchByTitle'],
            )
        return qs


class FilteredPropertiesListView (ListView):
    model = Listing
    queryset = Listing.posts.all()
    paginate_by = 25 # show 25 posts in reverse chronologial order
    template_name = "listing/properties.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.filter(
                purpose=self.request.GET['purpose'],
            )

        # SEARCH BY CATEGORY
        if self.request.GET['category']:
            if self.request.GET['category'] != 'any':
                qs = qs.filter(
                    category=self.request.GET['category']
                )
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


class CategoryListView (ListView):
    model = Listing
    queryset = Listing.posts.all()
    paginate_by = 25 # show 25 posts in reverse chronologial order
    template_name = "listing/properties.html"

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
        )
        return qs
        

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
    return render(request, 'listing/about-us.html')


def contact_us_page (request):
    if request.user.is_staff and request.user.is_authenticated:
        contacts = Contact.objects.all()
        contacts = contacts.order_by("-date_created").all()
        return render(request, 'listing/contactUs.html', {
            'contacts': contacts
        })
    return render(request, 'listing/contactUs.html')


def agents (request):
    agents = User.objects.all()
    return render(request, 'listing/agents.html', {
        'agents': agents
    })


@login_required
def createListing (request):
    heading = 'Sell Your Own Property'
    submit = 'Post'

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
                if listing_obj.custom_bedroom:
                    listing_obj.bedroom = ''
                elif bedroom:
                    listing_obj.bedroom = bedroom

                if (bedroom or listing_obj.custom_bedroom) and listing_obj.custom_bathroom:
                    listing_obj.bathroom = ''
                elif (bedroom or listing_obj.custom_bedroom) and bathroom:
                    listing_obj.bathroom = bathroom
            else:
                listing_obj.bedroom = ''
                listing_obj.bathroom = ''
            listing_obj.is_active = True
            listing_obj.save()

            for image_file in images:
                img = ListingImage(listing=listing_obj, image=image_file)
                img.save()

            messages.success(request, "Yeew, check it out on the home page!")
            return HttpResponseRedirect("/createListing")
        
        else:
            for field in listing_form:
                for error in field.errors:
                    messages.error(request, f"{field.name}: {error}")
            print(listing_form.errors)
            return render(request, 'listing/createListing.html', {
                'listing_form': listing_form,
                'heading': heading,
                'submit': submit,
                'create': True,
            })

    listing_form = listingForm
    return render(request, 'listing/createListing.html', {
        'listing_form': listing_form,
        'heading': heading,
        'submit': submit,
        'create': True,
    })

# Update Form Incomplete ## image ## bedroom and bathroom errors
@login_required
def updateListing (request, item_id):
    heading = 'Update Listing'
    submit = 'Save'
    listing = Listing.posts.get(id=item_id)

    if request.method == "POST":
        listing_form = listingForm (request.POST, instance=listing)
        images = request.FILES.getlist('images')
        bedroom = request.POST['bedroom']
        bathroom = request.POST.get('bathroom', None)
        category_list = ['house', 'flat', 'up', 'lp', 'fh', 'room', 'ph']

        if listing_form.is_valid():
            listing_obj = listing_form.save(commit=False)
            listing_obj.creator = request.user
            listing_obj.purpose = request.POST['purpose']

            if listing_obj.category in category_list:
                if listing_obj.custom_bedroom:
                    listing_obj.bedroom = ''
                elif bedroom:
                    listing_obj.bedroom = bedroom

                if (bedroom or listing_obj.custom_bedroom) and listing_obj.custom_bathroom:
                    listing_obj.bathroom = ''
                elif (bedroom or listing_obj.custom_bedroom) and bathroom:
                    listing_obj.bathroom = bathroom
            else:
                listing_obj.bedroom = ''
                listing_obj.bathroom = ''
            listing_obj.save()

            # No Image Update Option
            # for image_file in images:
            #     img = Image(listing=listing_obj, image=image_file)
            #     img.save()

            messages.success(request, "Listing has been updated!")
            return HttpResponseRedirect("/createListing")
        
        else:
            print(listing_form.errors)
            return render(request, 'listing/createListing.html', {
                'listing_form': listing_form,
                'heading': heading,
                'submit': submit,
            })

    listing_form = listingForm(instance=listing)
    return render(request, 'listing/createListing.html', {
        'listing_form': listing_form,
        'heading': heading,
        'submit': submit,
    })

@login_required
def deleteListing (request, item_id):
    listing = Listing.posts.get(id = item_id)
    if request.user == listing.creator:
        listing.is_active = False
        listing.save()
        messages.success(request, "Listing Has Been Deleted!")
        return redirect('/')
    else:
        message.error(request, "You don't have authority to delete this post.")
        return render(request, 'listing/singleProperty.html', {
        'post': listing,
        'active': False
    })

        
def privacyPolicy(request):
    return render(request, 'listing/privacy-policy.html')


def termsView(request):
    return render(request, 'listing/terms.html')