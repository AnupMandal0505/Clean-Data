from rest_framework.serializers import ModelSerializer
from app.models import User, StateTechnical,DistrictTechnical,TechnicalStaff
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','delete','is_staff','is_superuser','is_active','user_permissions','groups','last_login']



class StateTechnicalSerializer(ModelSerializer):
    user = UserSerializer()  
    class Meta:
        model = StateTechnical
        exclude = ['address']



class DistrictTechnicalSerializer(ModelSerializer):
    user = UserSerializer()  
    class Meta:
        model = DistrictTechnical
        exclude = ['address']


class StaffTechnicalSerializer(ModelSerializer):
    user = UserSerializer()  
    class Meta:
        model = TechnicalStaff
        exclude = ['address']
