from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

class Game(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(max_length = 255)
    url = models.URLField(max_length = 255, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    #highscores = models.ForeignKey(Highscore, on_delete=models.CASCADE, related_name="highscores")
    sales = models.PositiveIntegerField()
    developer = models.ForeignKey(User, related_name="games", blank=True)
    players = models.ManyToManyField(User, related_name="games_owned", blank=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Player(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    def __str__(self):
        return str(self.user.username)

class Developer(models.Model):
    user = models.OneToOneField(User, primary_key=True)


class Highscore(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
