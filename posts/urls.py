from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', views.PostApiViewSet, basename='posts')



urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', views.CommentApiViewSet.as_view({'get': 'list', 
                                                 'post': 'create'}), name='post-comments'),
    path('comments/<int:pk>/', views.CommentApiViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='comment-detail'),
]
