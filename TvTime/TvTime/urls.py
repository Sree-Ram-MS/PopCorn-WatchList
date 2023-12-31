"""
URL configuration for TvTime project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from user.views import loginpage
from django.conf import settings
from django.conf.urls.static import static

from MyLists.views import MoviesList
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router=DefaultRouter()
router.register(r'MYlist', MoviesList, basename='mvlist')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/',include('user.urls')),
    path('account/',include('account.urls')),
    # path('',loginpage.as_view(),name='login'),


    path('token-auth/', views.obtain_auth_token),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+router.urls
