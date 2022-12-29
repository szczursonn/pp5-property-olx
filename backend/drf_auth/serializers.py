from django.contrib.auth import authenticate
from users.models import User
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    
    email = serializers.CharField(
        write_only=True
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    

    def validate(self, attrs):
        email, password = attrs.get('email'), attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError('Wrong email or password', code='authorization')
        else:
            raise serializers.ValidationError('Email and password cannot be null', code='authorization')
        attrs['user'] = user
        return attrs

class RegisterSerializer(serializers.Serializer):
    
    email = serializers.CharField(
        write_only=True
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    username = serializers.CharField(
        write_only=True,
        required=False
    )
    phone_number = serializers.CharField(
        write_only=True,
        required=False
    )

    def validate(self, attrs):
        email, password, username, phone_number = attrs.get('email'), attrs.get('password'), attrs.get('username'), attrs.get('phone_number')

        if not username:
            username=email

        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                raise serializers.ValidationError('Email taken', code='authorization')
                
            user = User.objects.create_user(email=email, password=password, username=username, phone_number=phone_number)
        else:
            raise serializers.ValidationError('Email and password cannot be null', code='authorization')
        attrs['user']=user
        return attrs
