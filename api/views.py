from rest_framework import viewsets, filters
from api.models import Post, Comment, Group, Follow
from api.serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from api.permissions import OwnResourcePermission, OwnFollowerPermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [OwnResourcePermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group', None)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [OwnResourcePermission, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        queryset = Comment.objects.filter(post_id=post.id)
        return queryset


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [OwnResourcePermission]


# class FollowViewSet(viewsets.ModelViewSet):
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializer
#     permission_classes = [OwnFollowerPermission]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['user__username', ]

    # def create(self, request, *args, **kwargs):
    #     following = self.request.query_params.get('following')
    #     following_old = get_object_or_404(Follow, user=self.kwargs.get('user'), following=self.kwargs.get('following'))
    #     if following == following_old:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class APIFollow(APIView):
    permission_classes = [OwnFollowerPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]

    def get(self, request):
        follow = Follow.objects.all()
        serializer = FollowSerializer(follow, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        new_following = request.data['following']
        if serializer.is_valid():
            if Follow.objects.filter(user=request.user, following__username=new_following):
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)