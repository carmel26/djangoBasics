from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProfiles(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query') 
        
    skills = Skill.objects.filter(
        name__icontains= search_query
    )
    
    profiles = Profile.objects.distinct().filter(
         Q(name__icontains=search_query) | 
         Q(short_intro__icontains=search_query) |
         Q(skill__in=skills) 
        )
    return profiles, search_query





# request, profiles(objects sended), results(results perPage)
def paginateProfiles(request, profiles, results):
        
    page = request.GET.get('pageSend')
    
    # the number of data per page
    results = 3
    
    # initialisation of pagination objects
    paginator = Paginator(profiles, results)
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
        
    # this means we will have 3 buttons before the selected one's
    leftIndex = (int(page) - 3)
    
    if leftIndex < 1:
        leftIndex = 1
        
    # this +2 means we will have 2 button after the selected one's
    rightIndex = (int(page) + 2)
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)
    return custom_range, profiles