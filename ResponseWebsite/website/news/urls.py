from django.urls import path,include
from . import views

from django.urls import path

from rest_framework import routers


from django.urls import path
from django.urls import path




urlpatterns = [
    
   
    path('', views.homepage, name='homepage'),

 
    path('flood/',views.floods, name='floods'),
    path('earthquake/',views.earthquake, name='earthquake'),
    path('wildfire/',views.wildfire, name='wildfire'),
    path('storms/',views.storms, name='storms'),
    path('pandemic/',views.pandemic, name='pandemic'),
    path('violence/',views.violence, name='violence'),
    path('first-aid/',views.first_aid, name='first-aid'),
    path('relief/',views.Relief_help, name='rel-help'),
    path('relief2/',views.rel_help2, name='rel-help2'),
    path('email/',views.test_email,name='test_email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]