from django.db import models
from django.forms import ModelForm


# Models.
class User(models.Model):
    userid = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    registered = models.DateTimeField(auto_now_add=True, blank=True)


class UserArtist(models.Model):
    userid = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)
    artid = models.CharField(max_length=100)
    artname = models.CharField(max_length=100)
    traid = models.CharField(max_length=100)
    traname = models.CharField(max_length=100)


class Recommendations(models.Model):
    userid = models.CharField(max_length=100)
    recommendation = models.CharField(max_length=100)
    rating = models.IntegerField()
    recommendationType = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

# Forms
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['userid']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['userid', 'gender', 'age', 'country']
