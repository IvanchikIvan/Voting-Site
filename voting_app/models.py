from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Voting(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)


class Option(models.Model):
  voting_id = models.ForeignKey(Voting, on_delete=models.CASCADE)
  content = models.CharField(max_length=255)


class Vote(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  option = models.ForeignKey(Option, on_delete=models.CASCADE)
