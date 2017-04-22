from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import SignUpForm, AddGameForm
from django.template import RequestContext
from .models import Game, Ownedgame, Player, Highscore, User
from django.utils import timezone
from django.core.signing import Signer

from django.core.mail import send_mail

import time
import hashlib
from datetime import datetime

def developer_check(user):
    dev = get_object_or_404(Player, pk=user)
    tosi = dev.developer
    return tosi

def mainPage(request):
    return render(request, 'main_page.html')

def about(request):
    return render(request, 'about.html')

@login_required(login_url='/login/')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='/login/')
def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if Ownedgame.objects.filter(game_id=pk, user_id=request.user.id).count() == 0:
        return HttpResponseRedirect('/gamelist/')

    else:
        return render(request, 'game.html', {'game': game})

@user_passes_test(developer_check)
@login_required(login_url='/login/')
def addgame(request):

    context = RequestContext(request)

    if request.method == "POST":
        form = AddGameForm(request.POST)
        if form.is_valid():
            newgame = form.save(commit=False)
            newgame.developer = request.user
            newgame.date_published = timezone.now()
            newgame.save()
            return redirect('game_detail', pk=newgame.pk)
    else:
        form = AddGameForm()
    return render(request, 'addgame.html', {'form': form})

def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user.is_active = False
            user.save()
            signer = Signer()
            signed_value = signer.sign(user.pk)
            send_mail('Confirm registration to imma',
                      'Go to this URL to confirm your account: '
                      +'http://'+request.get_host()+'/signup_confirmed/'+str(signed_value),
                      'localhost',[user.email], fail_silently=False)

            confirmation_link = 'http://'+request.get_host()+'/signup_confirmed/'+str(signed_value)
            return render(request, 'confirm.html', {'confirmation_link' : confirmation_link})

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signup_confirmed(request, signed_value):
    """
    Activates a user when they open this view (which they received by mail).
    """
    try:
        signer = Signer()
        user_pk = signer.unsign(signed_value)
        user = User.objects.get(pk=user_pk)
        user.is_active = True
        user.save()
        return render(request, 'signup_confirmed.html')
    except:
        return HttpResponseRedirect("/denied")


@login_required(login_url='/login/')
def buyGame(request, game_id):

    context = RequestContext(request)
    user = request.user
    game = get_object_or_404(Game, id=game_id)
    pid = user.username + "-" + str(game.id) + "-" + str(time.time())
    amount = game.price
    sid = "imma2isbest"
    secret_key = "796c82d3e9b03deac64262b538ccea0f"

    # testing urls (comment when deployed in heroku)
    success_url = "http://localhost:5000/payment_succesfull"
    error_url = "http://localhost:5000/payment_failed"
    cancel_url = "http://localhost:5000/payment_cancelled"

    # production urls (uncomment when deployed in heroku)
    # success_url ="https://imma-game-service.herokuapp.com/payment_succesfull"
    # error_url = "https://imma-game-service.herokuapp.com/payment_failed"
    # cancel_url = "https://imma-game-service.herokuapp.com/payment_cancelled"

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

@login_required(login_url='/login/')
def payment_succesfull(request):

    context = RequestContext(request)
    pid = request.GET.get('pid', '').split("-")
    gameid = int(pid[1])
    buyer = pid[0]
    game = get_object_or_404(Game, id=gameid)

    user = request.user

    if str(user) != str(buyer):
        text = "Not your link!"
        url = "/"

    elif Ownedgame.objects.filter(game_id=gameid, user_id=user.id).count() == 0:
        boughtgame = Ownedgame(game_id=gameid, user_id=user.id)
        game.sales = game.sales + 1
        game.save()
        boughtgame.save()
        title = "Payment succesful"
        text = "Game added to your owned games"
        url = "/gamelist"
        linkText = "Go to gamelist"

    else:
        title = "Game already owned"
        url = "/gamelist"
        linkText = "Go to gamelist"

    return render(request, "message.html",
        {"title": title, "url": url, "text": text, "linkText": linkText}
        )


@login_required(login_url='/login/')
def payment_failed(request):
    # payment failed, what to do
    pass

@login_required(login_url='/login/')
def payment_cancelled(request):
    # payment cancelled, what to do
    pass

@login_required(login_url='/login/')
def gamesInStore(request):
    context = RequestContext(request)
    ownedGames = Ownedgame.objects.filter(user = request.user.id)
    context['UserGames'] = ownedGames

    ownedGameID = []
    for game in ownedGames:
        ownedGameID.append(int(game.game.id))


    games = Game.objects.all()
    context['AllGames'] = games
    games = games.exclude(id__in=ownedGameID)
    context['GamesAvailable'] = games
    return render_to_response("available_games.html", context)
