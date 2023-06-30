from django.urls import path
from .views import *

urlpatterns = [
    
    path('signin/',signinpage.as_view(),name="signin"),
    path("logout/",LogOut.as_view(),name='logout'),

]