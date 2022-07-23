from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.profiles, name="profiles"),
    path('profile/<str:primaryKey>', views.userProfile, name="userProfile"),
    
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    
    path('account/', views.userAccount, name="account"),
    path('edit-account/', views.editAccount, name="editAccount"),
    
    path('add-skill/', views.createSkill, name="createSkill"),
    path('update-skill/<str:primaryKey>/', views.updateSkill, name="updateSkill"),
    path('delete-skill/<str:primaryKey>/', views.deleteSkill, name="deleteSkill"),
]
