from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .form import ProjectForm

from .models import Project

projectsList = [
    {
        'id' : '1',
        'title' : "E-Commerce WebSite",
        'description' : "Fully functional ecommerce website",
    },
    {
        'id' : '2',
        'title' : "PortFolio Website",
        'description' : "This is a project where i built out my portfolio",
    },
    {
        'id' : '3',
        'title' : "M-Commerce Application",
        'description' : "Fully functional Mobile Application",
    },
    {
        'id' : '4',
        'title' : "Socil Network",
        'description' : "Awesome open source project im still working on",
    },
    {
        'id' : '5',
        'title' : "Business Man",
        'description' : "It has to be a person with a lot of quality",
    },
];


def projects(request):
    identification = "Carmel NKESHIMANA "
    projects = Project.objects.all
    context = {'message':identification, 'projects':projects}
    return render(request, 'projects/projects.html', context)

def project(request, primaryKey):
    projectObj = Project.objects.get(id=primaryKey);
    tags = projectObj.tags.all()
    context = {'projectObj': projectObj, 'tags' : tags}
    return render(request, 'projects/single-project.html',context)


def createProject(request):
    form = ProjectForm()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('projects')
            
        
    context = {'form':form}
    return render(request, "projects/project_form.html", context)


def updateProject(request, primaryKey):
    project = Project.objects.get(id = primaryKey)
    form = ProjectForm(instance = project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project) 
        if form.is_valid():
            form.save()
            return redirect('projects')
        
    context = {'form':form}
    return render(request, "projects/project_form.html", context)



def deleteProject(request, primaryKey):
    project = Project.objects.get(id=primaryKey)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {'object':project}
    return render(request, 'projects/delete_template.html', context)