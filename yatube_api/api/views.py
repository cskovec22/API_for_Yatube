from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, mixins, viewsets, generics

from posts.models import Follow, Group, Post, User
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer
)
from api.permissions import AuthorOrReadOnly


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    '''Кастомный вьюсет для создания подписки,
    получения списка подписок'''
    pass


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментария."""
    permission_classes = (AuthorOrReadOnly, IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_post(self):
        """Возвращает конкретный пост."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        """Возвращает queryset c комментариями для конкретного поста."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """"
        Создает комментарий к конкретному посту,
        где автор комментария - текущий пользователь.
        """
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )


class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        user = get_object_or_404(
            User,
            username=self.request.user.username
        )
        return user.follower

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class FollowList(generics.ListCreateAPIView):
#     """Вьюсет для подписки."""
#     # filter_backends = (filters.SearchFilter,)
#     # permission_classes = [IsAuthenticated]
#     # search_fields = ('following',)
#     queryset = User.objects.all()
#     serializer_class = FollowSerializer

#     # def get_queryset(self):
#     #     """
#     #     Возвращает queryset c подписками для конкретного пользователя.
#     #     """
#     #     user_follower = get_object_or_404(
#     #         User,
#     #         username=self.request.user.username
#     #     )
#     #     return user_follower.following

#     def perform_create(self, serializer):
#         """"
#         Подписывает пользователя, сделавшего запрос,
#         на пользователя, переданного в теле запроса.
#         """
#         serializer.save(
#             user=self.request.user
#         )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для сообщества."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для поста."""
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly, IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Создает пост, где автор - текущий пользователь."""
        serializer.save(author=self.request.user)
