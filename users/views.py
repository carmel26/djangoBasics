from multiprocessing import context
import profile
from django.shortcuts import render, redirect

# user part methods
from django.contrib.auth.decorators import login_required # for any view we want to block
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
# end users import
 
from django.contrib import messages 
from .form import CustomUserCreationForm, ProfileForm, SkillForm

from .models import Profile
from .utils import paginateProfiles, searchProfiles


# Create your views here.

# user part
def loginUser(request):
    page = 'login'
    context = {'page':page}
    # not allow a logged in user to go to login page
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Username doesn\'t exist')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # login function gone create a session of that user
            # and it gone add a cookie in our browser
            login(request, user)
            return redirect('profiles')
        else:
             messages.error(request,'Username or password is incorrect')
             
    return render(request, 'users/login_register.html',context)


def logoutUser(request):
    logout(request)
    messages.info(request,'User was logOut')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, "User account was created successfully!")
            
            # automatically loggin the user after registering
            login(request,user)
            return redirect('editAccount')
        
        else:
            messages.error(request, "Error was occurred during registration")
        
    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)


# profile part
def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    
    context = {'profiles':profiles, 
               'search_query':search_query, 
               'custom_range':custom_range}
    
    return render(request, 'users/profile.html',context)



def userProfile(request, primaryKey):
    profile = Profile.objects.get(id=primaryKey)
    
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    
    context = {'profile':profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)



# account part
@login_required(login_url='login')
def userAccount(request):
    profile =  request.user.profile
    
    skills = profile.skill_set.all() 
    projects = profile.project_set.all()
    
    context = {'profile':profile, 'skills':skills,'projects':projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            print("NOPE")
    
    context = {'form':form}
    return render(request, 'users/profile_form.html', context)


# skill part 
@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()
    profile = request.user.profile
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            messages.success(request, 'Skill was added successfully')
            skill.save()
            return redirect('account')
    
    context = {'form':form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request,primaryKey):
    profile = request.user.profile
    skill = profile.skill_set.get(id=primaryKey)
    form = SkillForm(instance = skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('account')
    
    context = {'form':form}
    return render(request, 'users/skill_form.html', context)


def deleteSkill(request, primaryKey):
    profile = request.user.profile
    skill = profile.skill_set.get(id=primaryKey)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')
    context = {'object':skill}
    return render(request, 'delete_template.html', context)