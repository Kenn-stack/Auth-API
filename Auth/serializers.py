from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'password', 'is_active', 'is_superuser', 'is_staff',]
        read_only_fields = ['is_superuser', 'is_active', 'is_staff',]
        extra_kwargs = {'password': {'write_only':True},'otp': {'write_only':True},}


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active', 'is_staff', 'is_superuser',]
        read_only_fields = ['email', 'user_id']


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password',]


class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField()
    password = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ActivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active','otp']
