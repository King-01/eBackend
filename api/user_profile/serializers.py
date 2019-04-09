# from drf_yasg.utils import swagger_serializer_method
import re
from rest_framework import serializers
from django.contrib.auth import authenticate


from .models import User

class TokenSerializer(serializers.Serializer):
    token = serializers.ReadOnlyField()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32,required=False)
    password = serializers.CharField(required=False)

    def validate(self,attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)

        user = None

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            raise serializers.ValidationError('Incomplete Credentials')

        if not user:
            raise serializers.ValidationError('Wrong Credentials')

        attrs['user'] = user
        return attrs


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32,required=True)
    first_name = serializers.CharField(max_length=32, required=True)
    lest_name = serializers.CharField(max_length = 32, required = False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=32,required=True)

    def validate_username(self, attrs):
        username = attrs.get('username', None)
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            raise serializers.ValueError('Invalid username')
        pass

    def validate_password(self,attrs):
        password = attrs.get('password', None)
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            raise serializers.ValueError('Password must contain atleast 8 characters, including atleast 1 uppercase and 1 lowercase alphabet, atleast 1 digit and a special character')

    def validate_email(self, attrs):
        email = attrs.get('email', None)
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email ):
            raise serializers.ValueError('Invalid E-mail address')

    def validate(self,attrs):
        pass

    def save(self, attrs):
        pass


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=32, required=True)
    new_password = serializers.CharField(max_length=32, required=True)
    confirm_password  =serializers.CharField(max_length=32, required=True)

    def validate_password(self, attrs):
        password_old = attrs.get('old_password', None)        
        password_new = attrs.get('new_password', None)
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password_old):
            raise serializers.ValueError('Old password is invalid')
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password_new):
            raise serializers.ValueError('New password is invalid')
        

    

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk', 'username', 'email', 'full_name', 'gender', 'bio',
            'institution', 'department', 'dob', 'role'
        )
        read_only_fields = (
            'username', 'email', 'gender', 'full_name'
        )


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk', 'full_name', 'bio', 'role', 'institution'
        )


class JournalDetailSerializer(serialziers.ModelSerializer):
    class Meta:
        model=Journals
        fields= (
            'title','year','authors_list','journal','indexed_in'
            )


class ConfrenceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= ConfrenceDetailSerializer
        fields= (
            'title','year','authors_list','description'
            )

class ProfileLinksDetailSerializer(serializers.ModelSerializer):
    class Meta:
        models=ProfileLinks
        fields = (
            'link_linked_in','link_research_gate','link_google_scholar','link_dblp','link_github','link_publons',
            )