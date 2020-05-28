from rest_framework import serializers
from .models import *

class ScopeOfWorkSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScopeOfWork
		fields ='__all__'

class InventorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Inventory
		fields = '__all__'

class CitySerializers(serializers.ModelSerializer):
	class Meta:
		model = City
		fields ='__all__'
		