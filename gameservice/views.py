from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# def signup(request):
# 	if request.method == 'POST':
# 		form = UserCreationForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data.get('username')
# 			raw_password = form.cleaned_data.get('password1')
# 			user = authenticate(username=username, password=raw_password)
# 			login(request, user)
# 			return redirect('home')
# 		else:
# 			form = UserCreationForm()
#
# 	return render(request, 'register.html', {'form': form})

def mainPage(request):
	return render(request, 'main_page.html')

def registerUser(request):

	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		# profile_form = UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()
			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			#KOMMENTOI POIS SEURAAVAT KAKSI RIVIÄ, JOS ET HALUA ERIKSEEN AKTIVOIDA ACCOUNTTIA!
			# user.is_active = False
			# sendConfirmEmail(user)
			user.save()
			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			# profile = profile_form.save(commit=False)
			profile.user = user
			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserProfile model.
			#if 'picture' in request.FILES:
			#	profile.picture = request.FILES['picture']
			# Now we save the UserProfile model instance.
			profile.save()
			# Update our variable to tell the template registration was successful.
			registered = True
		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			print(user_form.errors, profile_form.errors)
	# Not a HTTP POST, so we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		# profile_form = UserProfileForm()
	# Render the template depending on the context.
	if not registered:
		return render(request,
			'register.html',
			{
				'user_form': user_form,
				# 'profile_form': profile_form,
			}
		)

	else:
		return render(request,
			'main_page.html',
			{
				'title': "Thank you for registering!",
				'message': "ebin",
			}
		)

def loginUser(request):

	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/main_page_logged/')
			else:
				return render(request, 'message.html',
				{
				'title': "Account not activated",
				'message': "Please check your email and activate your account before logging in."
				})
		else:

			print ("Invalid login details: {0}, {1}".format(username, password))
			return render(request, 'message.html',
			{
			'title': "Invalid login details supplied",
			'message': "Please check your login information and try again."
			})

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
			# blank dictionary object...
			context['request'] = request
			context['user'] = request.user
			# If the user is authenticated, we'll sent the user to homepage
			if request.user.is_authenticated():
				return HttpResponseRedirect('/main_page_logged/')
			return render_to_response('login.html', {}, context)
