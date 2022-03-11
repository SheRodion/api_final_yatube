from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
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

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ModelViewSet):
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
