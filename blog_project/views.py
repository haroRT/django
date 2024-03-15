from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_jwt.settings import api_settings
from .serializers import PostSerializer, FileSerializer, ProfileSerializer, RegisterSerializer, UpdateProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from blog.models import Account ,Posts
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import BasePermission
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.exceptions import AuthenticationFailed
import os

class CustomJWTPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            auth_header = request.META['HTTP_AUTHORIZATION']
            token = auth_header.split(' ')[1] if auth_header.startswith('Bearer') else None
            decoded_jwt = jwt_decode_handler(token)
        except:
            return False
        request.user=decoded_jwt
        if request.user:
            return request.user
        return False
    

class CreateUserAPIView(APIView):
    def get(self, request):
        # Lấy tất cả các đối tượng từ cơ sở dữ liệu
        queryset = Account.objects.all()
        # Serialize các đối tượng
        serializer = RegisterSerializer(queryset, many=True)
        # Trả về response
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
         email = request.data['email']
         password = request.data['password']
         user = Account.objects.get(email=email)
         if user is not None and check_password(password,user.password):
            #  ham cua djangoJWT
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER 
            token = jwt_encode_handler({"email" :user.email,
                                        "role":user.role,
                                        "id":user.id
                                        })
            return Response({"token":token}, status=status.HTTP_200_OK)
         return Response({"error":"Login error"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([CustomJWTPermission])
def getProfile(request):
    user = request.user 
    profile = Account.objects.get(pk=user['id'])
    serializer = ProfileSerializer(profile)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([CustomJWTPermission])
def updateProfile(request):
    user = request.user 
    account = Account.objects.get(pk=user['id'])
    serializer = UpdateProfileSerializer(account,data =request.data ,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@permission_classes([CustomJWTPermission])
class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            # file_contents = uploaded_file.read()
            file_name = uploaded_file.name 
            # file_type = uploaded_file.content_type 
            
            public_dir = os.path.join(settings.MEDIA_ROOT, 'public')
            print(public_dir)
            if not os.path.exists(public_dir):
                os.makedirs(public_dir)
            
            file_path = os.path.join(public_dir, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            relative_file_path = os.path.join('public', file_name)

            return Response({'url': relative_file_path}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@permission_classes([CustomJWTPermission])
class PostAPIView(APIView):

    def post(self, request):
        serializer = PostSerializer(data=request.data,context={'user' :request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            post =Posts.objects.get(pk=pk,account_id= request.user['id'])
        except Posts.DoesNotExist:
            return Response({"error":"Delete error"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            post =Posts.objects.get(pk=pk,account_id= request.user['id'])        
            post.delete()
            return Response({"success":"Delete post successfully"},status=status.HTTP_204_NO_CONTENT)
        except Posts.DoesNotExist:
            return Response({"error":"Delete error"},status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def GetPostDetail(request,pk):
    try:
        post =Posts.objects.get(pk=pk)
        serializer=PostSerializer(post)
        return Response({"success":"get post successfully","post":serializer.data},status=status.HTTP_204_NO_CONTENT)
    except Posts.DoesNotExist:
        return Response({"error":"Get post error"},status=status.HTTP_404_NOT_FOUND)
    