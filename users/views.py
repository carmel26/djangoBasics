from multiprocessing import context
from django.shortcuts import render
from .models import Profile

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'users/profile.html',context)

def userProfile(request, primaryKey):
    profile = Profile.objects.get(id=primaryKey)
    
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    
    context = {'profile':profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)