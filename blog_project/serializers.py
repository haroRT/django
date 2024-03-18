from blog.models import Account, Comments, Posts
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
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
    

class FileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=10*1024*1024) 


class PostSerializer(serializers.ModelSerializer):
    account =RegisterSerializer(read_only =True)
    url =serializers.CharField(required=False,max_length=100)
    title =serializers.CharField(required=False,max_length=100)
    content =serializers.CharField(required=False,max_length=1000)
    class Meta:
        model =Posts
        fields =("id","title","content","url","account")

    def validate(self, attrs):
        if self.instance  is None:
            if attrs.get("content") is None and  attrs.get("url") is None :
                raise serializers.ValidationError("content and url cannot null post is not empty")
            return attrs
        else :
            return attrs
    
    def create(self, validated_data):
        user = self.context['user']
        account = Account.objects.get(id=user['id'])
        if account is None:
            raise("Cannot find account")
        post = Posts.objects.create(account=account,**validated_data)
        return post

class CommentSerializer(serializers.ModelSerializer):
    account =RegisterSerializer(read_only =True)
    url =serializers.CharField(required=False,max_length=100)
    content =serializers.CharField(required=False,max_length=1000)
    created =serializers.DateTimeField(read_only=True)
    post_id = serializers.IntegerField(required=True)
    class Meta:
        model =Comments
        fields =("id","content","url","account","created","post_id")

    def validate(self, attrs):
        if self.instance  is None:
            if attrs.get("content") is None and  attrs.get("url") is None :
                raise serializers.ValidationError("Content and url cannot null")
            return attrs
        else :
            return attrs
    
    def create(self, validated_data):
        try:
            post = Posts.objects.get(pk=validated_data.get('post_id'))
        except Posts.DoesNotExist:
            raise ValidationError("Cannot find post")
        user = self.context['user']
        account = Account.objects.filter(id=user['id']).first()
        if account is None:
            raise ValidationError("Cannot find account")
        comment = Comments.objects.create(account=account,**validated_data)
        return comment
