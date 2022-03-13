from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group, Follow
from .permissions import AuthorOrReadOnly
from .serializers import (
    PostSerializer, CommentSerializer,
    GroupSerializer, FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """Работа с постами (в т.ч. с авторизацией)"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Работа с группами"""
    permission_classes = (AuthorOrReadOnly,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Работа с комментариями к постам"""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin, viewsets.GenericViewSet):
    """Работа с подписками"""
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        get_user = self.request.user
        new_queryset = Follow.objects.filter(user=get_user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
