from email import message
from multiprocessing import context
from turtle import left, right, title
from django.contrib import messages 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required # for any view we want to block
from django.shortcuts import render, redirect
from .form import ProjectForm


from .utils import searchProject, paginateProjects
from .models import Project, Tag
 

def projects(request):
    projects, search_query = searchProject(request)
    custom_range, projects = paginateProjects(request, projects, 4)

    context = {'projects':projects, 
               'search_query':search_query,  
               'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, primaryKey):
    projectObj = Project.objects.get(id=primaryKey);
    tags = projectObj.tags.all()
    context = {'projectObj': projectObj, 'tags' : tags}
    return render(request, 'projects/single-project.html',context)

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES) 
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('account')
            
        
    context = {'form':form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def updateProject(request, primaryKey):
    profile = request.user.profile
    project = profile.project_set.get(id = primaryKey)
    form = ProjectForm(instance = project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('account')
        
    context = {'form':form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, primaryKey):
    profile = request.user.profile
    project = profile.project_set.get(id = primaryKey)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {'object':project}
    return render(request, 'delete_template.html', context)

