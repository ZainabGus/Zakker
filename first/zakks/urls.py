from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.zakk_feed, name='feed'),  # Пустой путь означает главную страницу внутри этого файла
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  #страница входа(в аккаунт)
    path('logout/', views.user_logout, name='logout'),  # страница выхода(из аккаунта)
    path('register/', views.register, name='register'), # страница регистрации
    path('profile/<str:username>/', views.profile, name='profile'),
    path('like/<int:zakk_id>/', views.toogle_like, name='toggle_like'),
    path('delete/<int:zakk_id>/', views.delete_zakk, name='delete_zakk'),
    path('edit/<int:zakk_id>/', views.edit_zakk, name='edit_zakk'),
    path('create/', views.create_zakk, name='create_zakk'),
]

#  path('register/', views.register, name='register'),
