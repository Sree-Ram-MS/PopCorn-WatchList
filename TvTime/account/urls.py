from django.urls import path
from .views import *


urlpatterns = [
    path('home/',Homepage.as_view(),name="Home"),
    path('homepage/',HomeContent.as_view(),name="First"),
    path('search/',MovieSearch.as_view(),name="Search"),
    path('profile/',Profile.as_view(),name='Profile'),
    path('ChangePSW/',ChangePassword.as_view(),name='Cpass'),
    path('fav/<int:movie_id>',Favlist,name="AddFav"),
    path('del/<int:fid>',delfav,name="DelFav"),

    path('Myfav/',MyFavlist.as_view(),name="MyFav"),

    path('MyWatchlist/',MyWatchList.as_view(),name="MyWatchlist"),
    path('watch/<int:movie_id>',AddWatchlist,name="Watchlist"),
    path('delwatch/<int:fid>',watched,name="DelWatch"),

]