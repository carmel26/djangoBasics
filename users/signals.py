
# work on signals imports
import profile
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
#end work on signals imports

from django.contrib.auth.models import User
from .models import Profile


# created will be a true or false value when the creation of the user is successfully 
#      added or not or a model it will check if it was successfully created or not
#  sender it gona be the model that send this
# instance of the model that actually trigger this or this object
#  ** kwargs 

# @receiver(post_save, sender=Profile)  #this is a decorator
def createProfile(sender, instance, created, **kwargs):
    print("Print signal is triggered")
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name
        )
    
    
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
    

# @receiver(post_delete, sender=Profile) #this is a decorator
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    print('Deleted...')
    
 
#  example of the trigger using methods 
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)