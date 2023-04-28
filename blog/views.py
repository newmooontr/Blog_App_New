from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer,CommentSerializer,LikeSerializer
from .models import Post, PostView,Comment,Like
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

# Create your views here.

class PostMVS(ModelViewSet):
    queryset = Post.objects.filter(is_published=True) 
    serializer_class = PostSerializer
    
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        postview = PostView.objects.filter(user= request.user, post= instance) 
        if not postview.exists(): 
            PostView.objects.create(post=instance, user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user = self.request.user
        serializer.validated_data['author_id'] = current_user.id
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    
    
class CommentMVS(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user = self.request.user
        post_id = self.kwargs.get('post_pk')
        print("post is=>", post_id)
        comment = Comment.objects.filter(post_id = post_id, commentor_id= current_user.id)
        if comment.exists(): # eğer yorum varsa 
            raise ValidationError(f" {current_user} is commented before") 
        else:                                       
            post_id = self.kwargs.get('post_pk') 
            serializer.validated_data['commentor_id'] = current_user.id 
            serializer.validated_data['post_id'] = post_id  
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def get_queryset(self):  
        post_id = self.kwargs.get('post_pk')
        if post_id == None: 
            return self.queryset 
        else:
            try:
                post = Post.objects.get(id=post_id) 
            except Post.DoesNotExist: 
              raise NotFound("A post with this id does not exist")
        return self.queryset.filter(post = post) 
    
    
   
class LikeMVS(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user = self.request.user
        post_id = self.kwargs.get('post_pk')
        like = Like.objects.filter(post_id = post_id, liker_id= current_user.id)
        if like.exists(): 
            raise Response (serializer.data)
        else:                                      
            post_id = self.kwargs.get('post_pk') 
            serializer.validated_data['liker_id'] = current_user.id 
            serializer.validated_data['post_id'] = post_id 
            serializer.validated_data['is_liked'] = True 
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        if self.request.user.id == instance.liker_id: 
            if instance.is_liked == True: 
                serializer.validated_data['is_liked'] = False 
            else:
                serializer.validated_data['is_liked'] = True  
                
        self.perform_update(serializer)
    
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
        

    
    
    