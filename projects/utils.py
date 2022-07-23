from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProject(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query') 
        
    tags = Tag.objects.filter(
        name__icontains = search_query
    )
    
    identification = "Carmel NKESHIMANA "
    
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in = tags)
    )
    return projects, search_query



# request, projects(objects sended), results(results perPage)
def paginateProjects(request, projects, results):
        
    page = request.GET.get('pageSend')
    
    # the number of data per page
    # results = 3
    
    # initialisation of pagination objects
    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
        
    # this means we will have 3 buttons before the selected one's
    leftIndex = (int(page) - 3)
    
    if leftIndex < 1:
        leftIndex = 1
        
    # this +2 means we will have 2 button after the selected one's
    rightIndex = (int(page) + 2)
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)
    return custom_range, projects