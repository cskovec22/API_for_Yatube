from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для поста."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ['id', 'author', 'text', 'pub_date', 'image', 'group']
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментария."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        fields = ['id', 'author', 'text', 'created', 'post']
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки."""
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = ['user', 'following']
        model = Follow
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
            )
        ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Ошибка! Подписка самого на себя.'
            )
        return data


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для сообщества."""

    class Meta:
        fields = ['id', 'title', 'slug', 'description']
        model = Group
