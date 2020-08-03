from rest_framework import serializers
from .models import bco_object_ieee_2791_2020

class Bco27912020Serializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object_ieee_2791_2020
        fields = ['object_id', 'payload']