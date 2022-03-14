from django.db import models
from django.conf import settings


# Create your models here.
class Authenticators(models.Model):
    X_Auth_Token = models.CharField(max_length=50)
    auth_key = models.CharField(max_length=50, null=True)


class GameServers(models.Model):
    auth_key = models.CharField(max_length=50)
    problem = models.IntegerField(null=True)
    time = models.IntegerField(null=True)
    status = models.CharField(max_length=15, null=True)


class WaitingLine(models.Model):
    auth_key = models.CharField(max_length=50)
    _id = models.IntegerField(null=True)
    _from = models.IntegerField(null=True)


class GameResult(models.Model):
    auth_key = models.CharField(max_length=50)
    win = models.IntegerField(null=True)
    lose = models.IntegerField(null=True)
    taken = models.IntegerField(null=True)


class UserInfo(models.Model):
    auth_key = models.CharField(max_length=50)
    _id = models.IntegerField(null=True)
    grade = models.IntegerField(null=True)
