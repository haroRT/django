from blog.models import Account
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):  # create class to serializer model
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Account.objects.all())]
    )

    username = serializers.CharField(
        max_length=100,
        required=True,
        validators=[UniqueValidator(queryset=Account.objects.all())]
    )

    password =serializers.CharField(required=True,max_length=100, write_only=True)

    class Meta:
        model = Account
        fields = ('id','username', 'email', 'password', 'fullname','avatar','cover_image','role')

    def validate(self, attrs):
        attrs['password'] =make_password(attrs['password'])
        attrs['role'] ='USER'
        return attrs

    def create(self, validated_data):
        account = Account.objects.create(**validated_data)
        return account

class ProfileSerializer(serializers.ModelSerializer):
    password =serializers.CharField(required=True,max_length=100, write_only=True)
    class Meta:
        model = Account
        fields = ('id','username', 'email', 'password', 'fullname','avatar','cover_image','role')

class UpdateProfileSerializer(serializers.ModelSerializer):
     
    fullname =serializers.CharField(required=False,max_length=100)
    avatar =serializers.CharField(required=False,max_length=300)
    cover_image =serializers.CharField(required=False,max_length=300)
    password =serializers.CharField(required=False,write_only=True)
    role =serializers.CharField(required=False,read_only=True)
    username =serializers.CharField(required=False,read_only=True)
    email = serializers.EmailField(
        write_only=True
    )
    class Meta:
        model = Account
        fields = ("__all__") 

    def update(self, instance, validated_data):
        if validated_data.get('fullname', instance.fullname) is not None :
            instance.fullname = validated_data.get('fullname', instance.fullname)
        if validated_data.get('avatar', instance.avatar) is not None :
            instance.avatar = validated_data.get('avatar', instance.avatar)
        if validated_data.get('cover_image', instance.avatar) is not None :
            instance.cover_image = validated_data.get('cover_image', instance.cover_image)
        instance.save()
        return instance