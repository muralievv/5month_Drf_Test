from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer, CommentSerializer, CommentCreateSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class PostPagination(PageNumberPagination):
    page_size = 5


class PostApiViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = PostPagination

    def get_queryset(self):
     if self.request.user.is_authenticated:
        return Post.objects.all()
     return Post.objects.filter(is_published=True)


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentApiViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CommentSerializer
        return CommentCreateSerializer
    
    
