from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import SignUpForm, AddGameForm
from django.template import RequestContext
from .models import Game, Ownedgame, Player, Highscore, User
from django.utils import timezone
from django.core.signing import Signer
from django.views.decorators.csrf import csrf_protect

from django.core.mail import send_mail

import time
import hashlib
from datetime import datetime

# ------------------------------------------------------------------
# functions that are used to check if user is a developer
# usage @dev_required before a view

def dev_required(fn=None):
    dec = user_passes_test(developer_check)
    if fn:
        return dec(fn)
    return dec

def developer_check(user):
    if user:
        dev = get_object_or_404(Player, pk=user)
        return dev.developer
    return False

# ------------------------------------------------------------------

# View to render the main page. Passes all games to the template
def mainPage(request):
    context = RequestContext(request)
    games = Game.objects.all()
    return render(request, 'main_page.html', {'games': games})

# View to render the about page
def about(request):
    return render(request, 'about.html')

# View to render the profile page. Login is required and if player
# has developer status and passes it as boolean value to template
@login_required(login_url='/login/')
def profile(request):
    dev = get_object_or_404(Player, pk = request.user)
    if dev.developer:
        devbool = True
    else:
        devbool = False
    return render(request, 'profile.html', {'devbool': devbool})

# View to redirect the user to game playing page. If user doesnt own the game
# redirects the user to shop
@login_required(login_url='/login/')
def game_detail(request, pk):

    scores = Highscore.objects.filter(game = pk).order_by('-score')[:5]
    game = get_object_or_404(Game, pk=pk)
    if Ownedgame.objects.filter(game_id=pk, user_id=request.user.id).count() == 0:
        return HttpResponseRedirect('/shop/')

    else:
        return render(request, 'game.html', {'game': game, 'scores': scores})

# View to add a new game, only displayed if user is developer. Otherwise
# redirects user to main page
@login_required(login_url='/login/')
def addgame(request):

    dev = get_object_or_404(Player, pk = request.user)
    if dev.developer:

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

    else:

        return HttpResponseRedirect('/')

# View to sign up the user, sends the confirmation email
def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data["applyAsDeveloper"]:
                player = Player(user = user, developer=True)
                player.save()
            else:
                player = Player(user = user, developer=False)
                player.save()

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

# If the link is clicked the confirmation is succesful and user is set to
# active status and can log in
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

# View to buy a game via simplepayments service. Uses a secret key and
# calculates a checksum that is validated by the payment service
@login_required(login_url='/login/')
def buyGame(request, game_id):

    context = RequestContext(request)
    user = request.user
    game = get_object_or_404(Game, id=game_id)
    pid = user.username + "-" + str(game.id) + "-" + str(time.time())
    amount = game.price
    sid = "imma2isbest"
    secret_key = "796c82d3e9b03deac64262b538ccea0f"

    success_url = 'http://'+request.get_host()+'/payment_succesfull'
    error_url = 'http://'+request.get_host()+'/payment_failed'
    cancel_url = 'http://'+request.get_host()+'/payment_cancelled'

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
    return render(request, "buy.html", {'context': context})

# -----------------------------------------------------------
# User is redirected to one of these views depending on the
# status that the payment service returns
@login_required(login_url='/login/')
def payment_succesfull(request):

    context = RequestContext(request)
    pid = request.GET.get('pid', '').split("-")
    gameid = int(pid[1])
    buyer = pid[0]
    game = get_object_or_404(Game, id=gameid)

    user = request.user

    if str(user) != str(buyer):
        title = "Cheater!"
        text = "Not your link!"
        gamebool = False

    # Succesful purchase, add game to ownedgames and add sales +1
    elif Ownedgame.objects.filter(game_id=gameid, user_id=user.id).count() == 0:
        boughtgame = Ownedgame(game_id=gameid, user_id=user.id)
        game.sales = game.sales + 1
        game.save()
        boughtgame.save()
        title ="Payment succesful"
        text = "Payment succesful, game added to your owned games"
        gamebool = True



    else:
        title = "Game already owned"
        text = "Return to library"
        gamebool = False


    return render(request, "game_bought.html",
        {"title": title, "text": text, "gamebool": gamebool, "gameid": gameid}
        )


@login_required(login_url='/login/')
def payment_failed(request):
    title = "Payment failed"
    text = "Return to library"
    return render(request, "game_bought.html",
        {"title": title, "text": text}
        )


@login_required(login_url='/login/')
def payment_cancelled(request):
    title = "Payment cancelled by user"
    text = "Return to library"
    return render(request, "game_bought.html",
        {"title": title, "text": text}
        )

# -----------------------------------------------------------

# view to display the games in store that user doesnt already own
@login_required(login_url='/login/')
def gamesInStore(request):
    context = RequestContext(request)
    ownedGames = Ownedgame.objects.filter(user = request.user.id)

    ownedGameID = []
    for game in ownedGames:
        ownedGameID.append(int(game.game.id))

    games = Game.objects.all()

    context['AllGames'] = games
    games = games.exclude(id__in=ownedGameID)
    context['GamesAvailable'] = games
    return render(request, "shop.html", {'context': context})

# View to display the developer view. Contains the list of developers own
# games
@login_required(login_url='/login')
def developerView(request):
    context = RequestContext(request)
    dev = get_object_or_404(Player, pk = request.user)
    if not dev.developer:
        return HttpResponseRedirect('/')
    else:
        devgames = Game.objects.filter(developer = request.user)
        context['devgames'] = devgames
        return render(request, "dev.html", {'context': context})

# View to display user owned games that the user can play
@login_required(login_url='/login/')
def myGames(request):

    context = RequestContext(request)
    usergames = Ownedgame.objects.filter(user = request.user)
    GameIDs = []
    for game in usergames:
        GameIDs.append(int(game.game.id))

    games = Game.objects.filter(id__in=GameIDs)

    context['UserGames'] = games
    return render(request, "library.html", {'context': context})

# View that is called when the iframe submits a highscore
# to the service
@csrf_protect
def submit_highscore(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    playerid = request.user

    if request.POST:
        scoretosave = request.POST.get('score')
        if scoretosave:
            Highscore(score = scoretosave, game = game, player=playerid).save()
            return HttpResponse('')
    return HttpResponseBadRequest

# View that is called when iframe submits a load request
# returns the savedata from database
@csrf_protect
def load(request, game_id):

    playerid = request.user
    ownedgame = get_object_or_404(Ownedgame, game = game_id, user = playerid)
    return HttpResponse(ownedgame.savedata)

# View that is called when iframe submits a save request
# the json data is parsed in javascript and text version is saved
# to the database
@csrf_protect
def save(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    playerid = request.user

    datatosave = request.POST['data']

    if datatosave:
        usergame = get_object_or_404(Ownedgame, game=game_id, user = playerid)
        usergame.savedata = datatosave
        usergame.save()
        return HttpResponse('')

    return HttpResponseBadRequest

# View that is used to delete a developers game
@dev_required
@login_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, id = game_id, developer = request.user)
    if game:
        game.delete()
    HttpResponseRedirect("/devpage/")
