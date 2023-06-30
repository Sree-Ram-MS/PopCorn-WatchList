from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializer import MovieModel
from .models import Movies
from account.models import Watchlist
from rest_framework import status,permissions,authentication

# Create your views here.
class MoviesList(ModelViewSet):
    serializer_class=MovieModel
    queryset=Watchlist.objects.all()
    model=Watchlist
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]