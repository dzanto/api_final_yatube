from rest_framework import viewsets, filters, generics
from api.models import Post, Comment, Group, Follow
from api.serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from api.permissions import OwnResourcePermission, OwnFollowerPermission
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [OwnResourcePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentAPI(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [OwnResourcePermission, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        queryset = Comment.objects.filter(post_id=post.id)
        return queryset


class GroupAPIView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [OwnResourcePermission]


class FollowAPIView(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [OwnFollowerPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

