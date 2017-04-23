from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from datetime import datetime, date

# Game model which contains all games that are added to service

class Game(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(max_length = 255)
    url = models.URLField(max_length = 255, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    sales = models.PositiveIntegerField(default=0)
    developer = models.ForeignKey(User, null=True)
    date_published = models.DateTimeField(auto_now_add=True)

# Model that contains all games that users have bought. Users can only
# play games that are found from the table with users id

class Ownedgame(models.Model):
    game = models.ForeignKey(Game, related_name="joku", null=True)
    user = models.ForeignKey(User, related_name="games_owned", null=True)
    purchasedate = models.DateTimeField(auto_now_add=True, auto_now=False)
    savedata = models.TextField(null=True, blank=True)

# Model that contains players, has one to one field to user and BooleanField
# for developer status

class Player(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    developer = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

# Model that holds all the highscores for all games. On each game page
# top 5 scores related to the game are displayed

class Highscore(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
