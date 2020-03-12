from django.db import models
from django.forms import ModelForm

class Item(models.Model):
    item = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item'


class User(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserRating(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_rating'


class Recommends(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    r_ui = models.CharField(max_length=255, blank=True, null=True)
    est = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recommends'

# Forms
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['user', 'password']
