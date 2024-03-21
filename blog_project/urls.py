"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path ,re_path
from .views import CommentAPIView, GetAllPost, GetPostDetail, PostAPIView, CreateUserAPIView, LoginView ,getProfile, updateProfile,FileUploadView

from django.views.static import serve


urlpatterns = [
     re_path(r'^public/public/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT + '/public',
    }),
    path('admin/', admin.site.urls),
    path('api/login', LoginView.as_view(), name='login'),
    path('api/user', CreateUserAPIView.as_view(), name='create_user'),
    path('api/profile', getProfile, name='create_user'),
    path('api/update-profile',updateProfile , name='update_user'),
    path('api/upload',FileUploadView.as_view() , name='upload'),
    path('api/post',PostAPIView.as_view() , name='post'),
    path('api/post/<int:pk>',PostAPIView.as_view() , name='detail'),
    path('api/post-detail/<int:pk>',GetPostDetail , name='detail'),
    path('api/all-post',GetAllPost , name='All'),

    path('api/comment/',CommentAPIView.as_view() , name='comment'),
    path('api/comment/<int:pk>',CommentAPIView.as_view() , name='detail'),

]
