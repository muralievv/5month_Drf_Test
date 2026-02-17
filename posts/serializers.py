from rest_framework import serializers
from .models import Post, Comment
from rest_framework.exceptions import ValidationError

class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created_at', 'updated_at', 'is_published']
        read_only_fields = ['author']

class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at', 'updated_at', 'is_approved']
        read_only_fields = ['author', 'post']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment 
        fields = ['id', 'body', 'created_at', 'updated_at', 'is_approved', 'post_id']
    def validate_post_id(self, post_id):
        try:
            Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError('Post with this id does not exist')
        return post_id
