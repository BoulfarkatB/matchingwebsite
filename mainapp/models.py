from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

    
class Hobby(models.Model):
    HOBBY_CHOICES = (
        ("Art", "Art"),
        ("Dancing", "Dancing"),
        ("Fishing", "Fishing"),
        ("Photography", "Photography"),
        ("Reading", "Reading"),
        ("Skydiving", "Skydiving"),
        ("Swimming", "Swimming"),
    )

    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Profile(models.Model):
    GENDERS = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    # A profile belongs to a single user
    user = models.OneToOneField(
        to=User,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    gender = models.CharField(max_length=8, choices=GENDERS)
    dob = models.CharField(max_length=10, default='')
    image = models.ImageField(upload_to='profile_images', blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    
    def __str__(self):
        # username associated with the profile    
        return self.user.username

## https://www.youtube.com/watch?v=2yoWf-kDXIk ## 
# A profile is created for each user
def createProfile(sender, **kwargs):
    if kwargs['created']:
       user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(createProfile, sender=User)
