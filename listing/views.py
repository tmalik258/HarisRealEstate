import json
from django.shortcuts import (render, redirect)
from django.http import (HttpResponse, HttpResponseRedirect)
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (authenticate, login, logout)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import Max
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.views.generic import (ListView, View)
from django.db.models import (BooleanField, Case, When, Q)

from .models import (Listing, ListingImage, ListingSpecification, ListingSpecificationValue, Category, Contact, Amenities,ListingAmenity)
from .forms import listingForm, listingGetRequestForm

from account.views import get_ip_address
from account.models import TrafficUser


# Create your views here.
def index (request):
	"""
	GET 10 RECENT LISTINGS
	"""
	posts = Listing.posts.all()[0:10]

	"""
	Store unique ip address in trafficuser model if already doesn't exists
	"""
	ip = get_ip_address(request)

	if not TrafficUser.objects.filter(user_ip__icontains=ip).exists():
		TrafficUser.objects.create(user_ip=ip)

	trafficCount = TrafficUser.objects.all().count()

	saleCount = Listing.posts.filter(specification_value__specification__name='Purpose', specification_value__value='Sale').count()

	rentCount = Listing.posts.filter(specification_value__specification__name='Purpose', specification_value__value='Rent out').count()

	return render(request, 'listing/index.html', {
		'posts': posts,
		'trafficCount': trafficCount,
		'saleCount': saleCount,
		'rentCount': rentCount,
	})


class PropertiesListView (ListView):
	model = Listing
	queryset = Listing.posts.all()
	paginate_by = 25 # show 25 posts in reverse chronologial order
	template_name = "listing/property_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		wishlist_listings = []
		if self.request.user.is_authenticated:
			wishlist_listings = self.request.user.user_wishlist.all()
		context['wishlist_listings'] = wishlist_listings
		return context


def property_detail (request, item):
    active = False

    try:
        post = Listing.posts.get(pk=item)

        # Check if the user has added the listing to their wishlist
        is_added_to_wishlist = False

        if request.user.is_authenticated:
            is_added_to_wishlist = post.user_wishlist.filter(id=request.user.id).exists()
            if request.user.username == post.creator.username:
                active = True

    except ObjectDoesNotExist:
        post = ""
    return render(request, 'listing/property_detail.html', {
        'post': post,
        'active': active,
        'is_added_to_wishlist': is_added_to_wishlist
    })

class SearchedPropertiesListView (ListView):
	model = Listing
	queryset = Listing.posts.all()
	paginate_by = 25 # show 25 posts in reverse chronologial order
	template_name = "listing/property_list.html"

	def get_queryset(self, **kwargs):
		qs = super().get_queryset(**kwargs)
		title_or_address_query = self.request.GET['searchByTitle']
		filtered_qs = qs.filter(
			Q(title__icontains=title_or_address_query) | 
			Q(address__icontains=title_or_address_query) |
			Q(price__icontains=title_or_address_query) |
			Q(category__name__icontains=title_or_address_query) |
			Q(area_size_unit__icontains=title_or_address_query) |
			Q(city__icontains=title_or_address_query) | 
			Q(specification_value__value__icontains=title_or_address_query) |
			Q(specification_value__specification__name__icontains=title_or_address_query) |
			Q(amenity__amenity__feature__icontains=title_or_address_query)
			).distinct()
		return filtered_qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		wishlist_listings = []
		if self.request.user.is_authenticated:
			wishlist_listings = self.request.user.user_wishlist.all()
		context['wishlist_listings'] = wishlist_listings
		return context


def is_valid_queryparam(param):
	return param != '' and param is not None


class FilteredPropertiesListView (ListView):
	model = Listing
	queryset = Listing.posts.all()
	paginate_by = 25 # show 25 posts in reverse chronologial order
	template_name = "listing/property_list.html"

	def get_queryset(self, **kwargs):
		qs = super().get_queryset(**kwargs)
		listing_form = listingGetRequestForm(self.request.GET)
		if listing_form.is_valid():
			purpose_query = self.request.GET['purpose']
			category_query = listing_form.cleaned_data['category_query']
			address_query = listing_form.cleaned_data['location']
			city_query = listing_form.cleaned_data['city']
			min_price_query = listing_form.cleaned_data['min_price']
			max_price_query = listing_form.cleaned_data['max_price']
			area_size = listing_form.cleaned_data['area_size']
			area_size_unit = listing_form.cleaned_data['area_size_unit']

			if is_valid_queryparam(purpose_query):
				qs = qs.filter(
						specification_value__specification__name='Purpose', specification_value__value__icontains=purpose_query
					)

			# SEARCH BY CATEGORY
			if is_valid_queryparam(category_query):
				qs = qs.filter(
					category__in=Category.objects.get(name=category_query).get_descendants(include_self=True)
				)
			# SEARCH BY LOCATION
			if is_valid_queryparam(address_query):
				qs = qs.filter(address__icontains=address_query)

			# SEARCH BY CITY
			if is_valid_queryparam(city_query):
				qs = qs.filter(city=city_query)

			# SEARCH BY PRICE MIN
			if is_valid_queryparam(min_price_query):
				qs = qs.filter(price__gte=min_price_query)

			# SEARCH BY PRICE MAX
			if is_valid_queryparam(max_price_query):
				qs = qs.filter(price__lt=max_price_query)

			# SEARCH BY AREA SIZE
			if is_valid_queryparam(area_size):
				qs = qs.filter(specification_value__specification__name='Area Size', specification_value__value=area_size)

			# SEARCH BY AREA SIZE
			if is_valid_queryparam(area_size_unit):
				qs = qs.filter(area_size_unit=area_size_unit)
		
		else:
			qs = qs.none()

		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		wishlist_listings = []
		if self.request.user.is_authenticated:
			wishlist_listings = self.request.user.user_wishlist.all()
		context['wishlist_listings'] = wishlist_listings
		return context


class CategoryListView (ListView):
	model = Listing
	queryset = Listing.posts.all()
	paginate_by = 25 # show 25 posts in reverse chronologial order
	template_name = "listing/property_list.html"

	def get_queryset(self, **kwargs):
		qs = super().get_queryset(**kwargs)

		qs = qs.filter(
			category__in=Category.objects.get(slug=self.kwargs['category_slug']).get_descendants(include_self=True)
		)

		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		wishlist_listings = []
		if self.request.user.is_authenticated:
			wishlist_listings = self.request.user.user_wishlist.all()
		context['wishlist_listings'] = wishlist_listings
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
	if request.method == "POST":
		listing_form = listingForm (request.POST, request.FILES)

		if listing_form.is_valid():
			listing_obj = listing_form.save(commit=False)
			listing_obj.creator = request.user # User
			listing_obj.is_active = True # Is Active
			listing_obj.is_sold = False # Is Sold
			listing_obj.save()

			# Fetch or cache the ListingSpecification objects
			specifications = cache.get('listing_specifications')
			if not specifications:
				specifications = ListingSpecification.objects.all()
				cache.set('listing_specifications', specifications)

			# Create a list of ListingSpecificationValue objects
			specification_values = [
				ListingSpecificationValue(
					listing=listing_obj,
					specification=specifications.get(name='Purpose'),
					value=listing_form.cleaned_data['purpose']
				),
				ListingSpecificationValue(
					listing=listing_obj,
					specification=specifications.get(name='Area Size'), value=listing_form.cleaned_data['area_size']
				),
			]

			furnished = listing_form.cleaned_data['furnished']
			if furnished:
				specification_values += [
					ListingSpecificationValue(
						listing=listing_obj,
						specification=specifications.get(name='Furnished'),
						value=listing_form.cleaned_data['furnished']
					),
					ListingSpecificationValue(
						listing=listing_obj,
						specification=specifications.get(name='Construction State'), value=listing_form.cleaned_data['state']
					),
				]

			floor_levels = listing_form.cleaned_data['custom_floor']
			if floor_levels:
				specification_values += [
					ListingSpecificationValue(
						listing=listing_obj,
						specification=specifications.get(name='Floors'), value=floor_levels
					),
				]
			
			beds = listing_form.cleaned_data['custom_bedroom']
			baths = listing_form.cleaned_data['custom_bathroom']

			if beds:
				if baths:
					specification_values += [
							ListingSpecificationValue(
							listing=listing_obj,
							specification=specifications.get(name='Bedroom'), value=beds
						),
						ListingSpecificationValue(
							listing=listing_obj,
							specification=specifications.get(name='Bathroom'), value=baths
						),
					]
				else:
					specification_values += [
							ListingSpecificationValue(
							listing=listing_obj,
							specification=specifications.get(name='Bedroom'), value=beds
						),
					]


			# Bulk create the ListingSpecificationValue objects
			ListingSpecificationValue.objects.bulk_create(specification_values)

			# Fetch the selected amenities as a list
			selected_amenities = request.POST.getlist('amenities') # Amenities
			if selected_amenities:
				amenities = cache.get('listing_amenities')
				if not amenities:
					amenities = Amenities.objects.all()
					cache.set('listing_amenities', amenities)
				
				amenities_values = []
				
				# # Iterate over the selected amenities
				for s_amenity in selected_amenities:
					amenities_values += [
						ListingAmenity(
							listing=listing_obj,
							amenity=amenities.get(feature=s_amenity)
						),
					]
				
				ListingAmenity.objects.bulk_create(amenities_values)


			# if listing_obj.category in category_list:
			#     if listing_obj.custom_bedroom:
			#         listing_obj.bedroom = ''
			#     elif bedroom:
			#         listing_obj.bedroom = bedroom

			#     if (bedroom or listing_obj.custom_bedroom) and listing_obj.custom_bathroom:
			#         listing_obj.bathroom = ''
			#     elif (bedroom or listing_obj.custom_bedroom) and bathroom:
			#         listing_obj.bathroom = bathroom
			# else:
			#     listing_obj.bedroom = ''
			#     listing_obj.bathroom = ''

			# Iterate over the images
			images = request.FILES.getlist('images')
			for image_file in images:
				img = ListingImage(listing=listing_obj, image=image_file)
				img.save()


			messages.success(request, "Ad has been posted successfully!")
			return redirect('account:profile')
		
		else:
			return render(request, 'listing/createListing.html', {
				'form': listing_form,
			})

	listing_form = listingForm()
	return render(request, 'listing/createListing.html', {
		'form': listing_form,
	})

# Update Form Incomplete ## image ## bedroom and bathroom errors
@login_required
def updateListing (request, item_id):
	listing = Listing.posts.get(pk=item_id)

	if request.user == listing.creator:
		if request.method == "POST":
			listing_form = listingForm (request.POST, instance=listing)

			if listing_form.is_valid():
				listing_form.is_sold = False # Is Sold
				listing_form.save()

				# Fetch or cache the ListingSpecification objects
				specifications = cache.get('listing_specifications')
				if not specifications:
					specifications = ListingSpecification.objects.all()
					cache.set('listing_specifications', specifications)

				# Delete the list of ListingSpecificationValue objects
				ListingSpecificationValue.objects.filter(listing=listing).delete()

				# Create a list of ListingSpecificationValue objects
				specification_values = [
					ListingSpecificationValue(
						listing=listing,
						specification=specifications.get(name='Purpose'),
						value=listing_form.cleaned_data['purpose']
					),
					ListingSpecificationValue(
						listing=listing,
						specification=specifications.get(name='Area Size'), value=listing_form.cleaned_data['area_size']
					),
				]

				furnished = listing_form.cleaned_data['furnished']
				if furnished:
					specification_values += [
						ListingSpecificationValue(
							listing=listing,
							specification=specifications.get(name='Furnished'),
							value=listing_form.cleaned_data['furnished']
						),
						ListingSpecificationValue(
							listing=listing,
							specification=specifications.get(name='Construction State'), value=listing_form.cleaned_data['state']
						),
					]

				floor_levels = listing_form.cleaned_data['custom_floor']
				if floor_levels:
					specification_values += [
						ListingSpecificationValue(
							listing=listing,
							specification=specifications.get(name='Floors'), value=floor_levels
						),
					]
				
				beds = listing_form.cleaned_data['custom_bedroom']
				baths = listing_form.cleaned_data['custom_bathroom']

				if beds:
					if baths:
						specification_values += [
								ListingSpecificationValue(
								listing=listing,
								specification=specifications.get(name='Bedroom'), value=beds
							),
							ListingSpecificationValue(
								listing=listing,
								specification=specifications.get(name='Bathroom'), value=baths
							),
						]
					else:
						specification_values += [
								ListingSpecificationValue(
								listing=listing,
								specification=specifications.get(name='Bedroom'), value=beds
							),
						]


				# Bulk create the ListingSpecificationValue objects
				ListingSpecificationValue.objects.bulk_create(specification_values)

				# Fetch the selected amenities as a list
				ListingAmenity.objects.filter(listing=listing).delete()
				selected_amenities = request.POST.getlist('amenities') # Amenities
				if selected_amenities:
					amenities = cache.get('listing_amenities')
					if not amenities:
						amenities = Amenities.objects.all()
						cache.set('listing_amenities', amenities)
					
					amenities_values = []
					
					# # Iterate over the selected amenities
					for s_amenity in selected_amenities:
						amenities_values += [
							ListingAmenity(
								listing=listing,
								amenity=amenities.get(feature=s_amenity)
							),
						]
					
					ListingAmenity.objects.bulk_create(amenities_values)

				# Iterate over the images
				# images = request.FILES.getlist('images')
				# for image_file in images:
				# 	img = ListingImage(listing=listing, image=image_file)
				# 	img.save()


				messages.success(request, "Ad has been Updated successfully!")
				return redirect('account:profile')
			
			else:
				return render(request, 'listing/edit_listing.html', {
					'form': listing_form,
				})

		listing_form = listingForm(instance=listing, initial={
			'area_size': listing.get_area_size(),
			'purpose': listing.get_purpose(),
			'custom_bedroom': listing.get_bedroom(),
			'custom_bathroom': listing.get_bathroom(),
			'custom_floor': listing.get_floor(),
			'furnished': listing.get_furnished(),
			'state': listing.get_construction_state(),
		})
		amenities_fields = ListingAmenity.objects.filter(listing=listing)
		amenities_list = []
		for amenity in amenities_fields:
			amenities_list.append(amenity.amenity.feature)
		amenities_json = json.dumps(amenities_list)

		return render(request, 'listing/edit_listing.html', {
			'form': listing_form,
			'amenities': amenities_json,
			'category': listing.category
		})
	else:
		messages.error(request, 'You are not authorized to edit this listing')
		return redirect('listing:index')

@login_required
def deleteListing (request, item_id):
    listing = Listing.posts.get(pk=item_id)
    if request.user == listing.creator:
        listing.is_active = False
        listing.save()
        messages.success(request, "Ad Has Been Deleted!")
        return redirect('account:profile')
    else:
        message.error(request, "Sorry! You don't have privilege to delete this ad.")
        return render(request, 'listing/property_detail.html', {
            'post': listing,
            'active': False
        })

        
def privacyPolicy(request):
    return render(request, 'listing/privacy-policy.html')


def termsView(request):
    return render(request, 'listing/terms.html')