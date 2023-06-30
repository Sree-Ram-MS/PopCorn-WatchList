from rest_framework import serializers
from .models import *
from account.models import Watchlist
from django.contrib.auth.models import User

class Movieserializer(serializers.Serializer):
    m_id = serializers.IntegerField()


class MovieModel(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = "__all__"