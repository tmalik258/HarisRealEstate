from django.contrib import messages
from django.shortcuts import (render, redirect)
from django.http import (HttpResponse, JsonResponse)
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import (login, logout)
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import (force_bytes, force_str)
from django.utils.http import (urlsafe_base64_decode, urlsafe_base64_encode)
from django.db.models import BooleanField, Case, When
from django.views.generic import ListView

from .models import User
from .forms import (RegistrationUserForm, RegisterationProfileForm, ProfileEditForm)
from .token import account_activation_token

# Listing App
from listing.models import Listing

# Create your views here.
class WishlistView(LoginRequiredMixin, ListView):
	model = Listing
	template_name = 'listing/property_list.html'
	paginate_by = 12

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['heading'] = 'Your Wishlist'
		return context

	def get_queryset(self, *kwargs):
		qs = Listing.posts.filter(user_wishlist=self.request.user)
		qs = qs.annotate(is_in_wishlist=Case(
			When(user_wishlist__id=self.request.user.id, then=True),
			default=False,
			output_field=BooleanField(),
		))
		return qs


@login_required
def Add_to_wishlist_view(request, item):
	try:
		post = Listing.posts.get(pk=item)
		if post.user_wishlist.filter(id=request.user.id).exists():
			post.user_wishlist.remove(request.user)
			print('removed from wishlist')
		else:
			post.user_wishlist.add(request.user)
			print('added to wishlist')

	except ObjectDoesNotExist:
		messages.error(request, 'Listing doesn\'t exist.')

	return redirect(request.META['HTTP_REFERER'])


@login_required
def edit_details(request):
	if request.method == 'POST':
		user_form = ProfileEditForm(instance=request.user, data=request.POST)
		if user_form.is_valid():
			user_form.save()
	else:
		user_form = ProfileEditForm(instance=request.user)

	return render(request, 'account/user/edit_details.html', {
		'form': user_form
	})


@login_required
def delete_user(request):
	user = User.objects.get(email=request.user)
	user.is_active = False
	user.save()
	logout(request)
	return redirect('account:delete_confirm')


class CustomLoginView(LoginView):
	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			next_url = self.request.GET.get('next')
			if next_url != None:
				return redirect(next_url)
			else:
				return redirect('listing:index')
		return super().dispatch(request, *args, **kwargs)

	def form_invalid(self, form):
		try:
			user = User.objects.get(email=form.cleaned_data.get('username'))
			# Check if the user is active
			if not user.is_active and not user.is_verified:
				# Resend verification email to the user
				# Setup email
				current_site = get_current_site(self.request)
				subject = 'Activate your Account'
				# user = self.request.user
				message = render_to_string('account/registration/account_verification_resent_email.html', {
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': account_activation_token.make_token(user),
				})
				user.send_verification_email(subject=subject, message=message)
				# Add a message to inform the user about the email resent
				messages.info(self.request, 'A verification email has been resent. Please check your email and activate your account.')
				self.user.send_verification_email(self.request.user)
				
				
				# Redirect the user to a page indicating that the verification email has been resent
				return redirect('account:login')
		except:
			pass
		
		return super().form_invalid(form)

	def get_success_url(self):
		# Get the value of the 'next' parameter from the request's GET parameters
		next_url = self.request.GET.get('next')

		if next_url != None:
			return next_url
		else:
			return reverse('listing:index')


def register(request):
	if request.user.is_authenticated:
		return redirect('/')

	if request.method == "POST":
		user_form = RegistrationUserForm(request.POST)
		profile_form = RegisterationProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			# user setup
			user = user_form.save(commit=False)
			user.email = user_form.cleaned_data['email']
			user.set_password(user_form.cleaned_data['password'])
			user.is_active = False
			user.is_verified = False
			user.save()

			# profile setup
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()

			# Setup email
			current_site = get_current_site(request)
			subject = 'Activate your Account'
			message = render_to_string('account/registration/account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.send_verification_email(subject=subject, message=message)
			messages.success(request, 'Your account has been created successfully. Please check your mail for account verification')
			return redirect('listing:index')
		else:
			return render(request, 'account/registration/register.html', {
				'form': user_form,
				'profile_form': profile_form
			})

	user_form = RegistrationUserForm()
	profile_form = RegisterationProfileForm()
	return render(request, 'account/registration/register.html', {
		'form': user_form,
		'profile_form': profile_form
	})


def account_activate(request, uid64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uid64))
		user = User.objects.get(pk=uid)
	except():
		pass
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.is_verified = True
		user.save()
		messages.success(request, 'Your account has been verified.')
		login(request, user)
		return redirect('account:profile')
	else:
		messages.error(request, 'Invalid User/token')
		return redirect('account:login')
		# return render(request, 'account/registration/activation_invalid.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect("listing:index")


class profileWithPropertiesListView(ListView, LoginRequiredMixin):
    model = Listing
    paginate_by = 25 # show 25 posts in reverse chronologial order
    template_name = "account/user/profile.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.filter(
                creator=self.request.user,
                is_active=True
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
            return redirect('account:profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'user/profile-update.html',{
        'u_form': u_form,
        'p_form': p_form
    })
