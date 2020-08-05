from rest_framework import serializers
from .models import bco_object_ieee_2791_2020

class BcoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object_ieee_2791_2020
        fields = ['object_id', 'payload', 'state']

class BcoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object_ieee_2791_2020
        fields = ['object_id', 'payload', 'state']

class BcoPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object_ieee_2791_2020
        fields = ['object_id', 'payload', 'state']

class BcoDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object_ieee_2791_2020
        fields = ['object_id', 'payload', 'state']