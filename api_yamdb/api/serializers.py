from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Comment, Review
from reviews.constants import MAX_SCORE, MIN_SCORE

User = get_user_model()


# class TitleReadSerializer(serializers.ModelSerializer):
#     ...
#     rating = serializers.IntegerField()
#     ...


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, score):
        if score < MIN_SCORE or score > MAX_SCORE:
            raise serializers.ValidationError(
                f'Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}'
            )
        return score

    def validate(self, attrs):
        author = self.context['request'].user
        title = self.context['view'].kwargs.get('title_id')
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(author=author, title=title).exists()
        ):
            raise serializers.ValidationError(
                'Нельзя написать два отзыва на произведение'
            )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
