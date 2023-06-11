from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    
    path('', views.home, name="home"),
    path('create-post/', views.create_post, name="create-post"),
    path('update-post/<str:pk>/', views.update_post, name="update-post"),
    path('delete-post/<str:pk>/', views.delete_post, name="delete-post"),
    path('like-post/<str:pk>/', views.like_post, name="like-post"),   
]