from rest_framework import serializers

from .models import Post, Comment, Group, Follow
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    # following = serializers.ReadOnlyField(source='following.username')
    following = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field='username')
    user = serializers.ReadOnlyField(source='user.username')
    # following = serializers.CharField(source='following.username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Follow

#
#     # user = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
#     # following = serializers.SlugRelatedField(many=False, queryset=Follow.objects.all(), slug_field='username')
#
#     # user = serializers.CharField(source='user.username')
#     # following = serializers.CharField(source='following.username')
#