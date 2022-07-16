from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user.username)


class Lead(models.Model):
    ismi = models.CharField(max_length=255)
    familiasi = models.CharField(max_length=255)
    yoshi = models.IntegerField(default=0)
    profil = models.ForeignKey(UserProfil, on_delete=models.CASCADE)
    agent = models.ForeignKey('Agent', null=True, blank=True, on_delete=models.SET_NULL)
    kategoriya = models.ForeignKey('Category', related_name='leads',null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.familiasi 


class Category(models.Model):
    nomi = models.CharField(max_length=50)
    profil = models.ForeignKey(UserProfil, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomi


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profil = models.ForeignKey(UserProfil, on_delete=models.CASCADE)
    
    def __str__(self): 
        return str(self.user)
        

def user_created(sender, instance, created, **kwargs):
    if created:
        UserProfil.objects.create(user = instance)

post_save.connect(user_created, sender=User)
    


    