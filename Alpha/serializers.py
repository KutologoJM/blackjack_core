from . import models
from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Player
        fields = '__all__'


class HandSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.Player.objects.all()
    )

    class Meta:
        model = models.Hand
        fields = '__all__'

