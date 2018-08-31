from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('join', views.sign_up, name='sign_up'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('comment/<username>', views.comment, name='comment'),
    path('<username>', views.profile, name='profile'),
]
