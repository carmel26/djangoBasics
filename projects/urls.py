from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name="projects"), 
    path('project/<str:primaryKey>/', views.project, name="project"),
    
    path('create-project/', views.createProject, name="createProject"),
    path('update-project/<str:primaryKey>', views.updateProject, name="updateProject"),
    path('delete-project/<str:primaryKey>', views.deleteProject, name="deleteProject"),
]
