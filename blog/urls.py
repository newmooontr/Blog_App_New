
from django.urls import path, include
from rest_framework import routers
from .views import PostMVS,CommentMVS,LikeMVS


router = routers.DefaultRouter() 


router.register('posts', PostMVS)
# router.register('comments/', CommentMVS) 
# router.register('likes/', LikeMVS)



urlpatterns = [
    
]
urlpatterns += router.urls

