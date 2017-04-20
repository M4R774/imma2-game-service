from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, AddGameForm
from django.template import RequestContext
from .models import *
from django.utils import timezone

import time
import hashlib
from datetime import datetime


def mainPage(request):
    return render(request, 'main_page.html')

def about(request):
    return render(request, 'about.html')

def profile(request):
    return render(request, 'profile.html')

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'game.html', {'game': game})

def addgame(request):

    context = RequestContext(request)

    if request.method == "POST":
        form = AddGameForm(request.POST)
        if form.is_valid():
            newgame = form.save(commit=False)
            newgame.author = request.user
            newgame.published_date = timezone.now()
            newgame.save()
            return redirect('game_detail', pk=newgame.pk)
    else:
        form = AddGameForm()
    return render(request, 'addgame.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('mainpage')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


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
            print(user_form.errors)
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


@login_required
def buyGame(request, gameid):

    context = RequestContext(request)
    user = request.user
    game = get_object_or_404(Game, id=gameid)
    pid = user.username
    # pid = user.username + "-" + str(game.id) + "-" + str(time.time())
    amount = game.price
    sid = "imma2isbest"
    secret_key = "796c82d3e9b03deac64262b538ccea0f"

    success_url = "http://localhost:5000/"
    error_url = "http://localhost:5000/"
    cancel_url = "http://localhost:5000/"

    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = hashlib.md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    context['pid'] = pid
    context['sid'] = sid
    context['amount'] = amount
    context['checksum'] = checksum
    context['success_url'] = success_url
    context['cancel_url'] = cancel_url
    context['error_url'] = error_url
    context['game'] = game
    context['checksumstr'] = checksumstr
    return render_to_response("buy.html", context)

@login_required
def payment_succesfull(request):

    context = RequestContext(request)
    pid = request.GET.get('pid', '').split("-")
    game_id = int(pid[1])
    buyer = pid[0]
    game = get_object_or_404(Game, id=gameid)
    user = context['user']

    if str(user) != str(buyer):
        # trying to use false buy link, what to do
        pass
    elif Game.objects.filter(gameid=game.id, players=user.id).count() == 0:
        boughtgame = Game(gameid=game.id, players=user.id)
        boughtgame.save()
    else:
        # game already owned, what to do
        pass


@login_required
def payment_failed(request):
    # payment failed, what to do
    pass

@login_required
def payment_cancelled(request):
    # payment cancelled, what to do
    pass

@login_required
def gamesInStore(request):
    context = RequestContext(request)
    ownedGames = Game.objects.filter(players=request.user)
    context['UserGames'] = ownedGames

    ownedGameID = []
    for game in ownedGames:
        ownedGameID.append(int(game.game.id))

    games = Game.objects.all()
    games = games.exclude(id__in=ownedGameID)
    context['GamesAvailable'] = games
    return render(request, 'available_games.html', {'games':games} )
