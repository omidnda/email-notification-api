from rest_framework import serializers
from .models import  Newsletter, CustomUser
#========================================================
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user=CustomUser.objects.create_user(
            email = validated_data["email"],
            password = validated_data["password"],
        )
        return user
    
class UserAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)
    active_code = serializers.CharField(max_length=10)
#========================================================
class NewsletterSubscriberSerializer(serializers.Serializer):
        email = email = serializers.EmailField()
        subscribed_newletter = serializers.BooleanField()

#========================================================
class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'
#========================================================