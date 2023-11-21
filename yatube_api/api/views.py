from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets

from .permissions import AuthorPermission
from posts.models import Group, Post
import api.serializers as sl


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = sl.PostSerializer
    permission_classes = [permissions.IsAuthenticated,
                          AuthorPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = sl.GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = sl.CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          AuthorPermission]

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
