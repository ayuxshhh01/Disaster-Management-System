from django.urls import path,include
from . import views
from .views import prediction_view
# from django.urls import path
# from .views import map_view, hospital_locations
from rest_framework import routers

# router  = routers.DefaultRouter()
# router.register('news',views.relevanceview)


urlpatterns = [
    path('', views.homepage, name='news-home'),
   
    path('message/',views.message, name='alert'),
 
    path('flood/',views.floods, name='floods'),
    path('earthquake/',views.earthquake, name='earthquake'),
    path('wildfire/',views.wildfire, name='wildfire'),
    path('storms/',views.storms, name='storms'),
    path('pandemic/',views.pandemic, name='pandemic'),
    path('violence/',views.violence, name='violence'),
    path('first-aid/',views.first_aid, name='first-aid'),
    path('relief/',views.Relief_help, name='rel-help'),
    path('relief2/',views.Relief_help2, name='rel-help2'),
    path('email/',views.test_email,name='test_email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/predict/', prediction_view, name='predict')
]
    # path('map/', map_view, name='map_view'),
    # path('hospitals/', hospital_locations, name='hospital_locations'),