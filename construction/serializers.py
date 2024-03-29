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
		
class InquirySerializers(serializers.ModelSerializer):
	class Meta:
		model = Inquiry
		fields = ('name', 'phone', 'email', 'message')

class NotificationSerializers(serializers.ModelSerializer):
	class Meta:
		model = Notification
		fields = '__all__'