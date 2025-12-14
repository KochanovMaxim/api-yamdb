from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('author', 'title', 'pub_date')

    def validate(self, attrs):
        if self.context['request'].method != 'POST':
            return attrs

        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')

        try:
            title = Title.objects.get(id=title_id)
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    'Нельзя написать два отзыва на произведение'
                )
        except Title.DoesNotExist:
            pass

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        read_only_fields = ('author', 'review', 'pub_date')
