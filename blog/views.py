from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from .models import Post, PostView
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class PostMVS(ModelViewSet):
    queryset = Post.objects.filter(is_published=True) 
    serializer_class = PostSerializer
    
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user = self.request.user
        serializer.validated_data['author_id'] = current_user.id
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        postview = PostView.objects.filter(user= request.user, post= instance) 
        if not postview.exists(): 
            PostView.objects.create(post=instance, user=request.user) 
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    
class CommentMVS(ModelViewSet):
    pass
    
    
class LikeMVS(ModelViewSet):
    pass