from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

from api.serializers import (CommentSerializer, ReviewSerializer)
from reviews.models import Review, Title


# from django.db.models import Avg
# class TitleViewSet(viewsets.ModelViewSet):
#     ...
#     queryset = Title.objects.annotate(rating=Avg('reviews__score'))
#     ...


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = PageNumberPagination
    # Добавить пермишены, когда их сделают

    def get_review_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def get_queryset(self):
        title = self.get_review_title()
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = self.get_review_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = PageNumberPagination
    # Добавить пермишены, когда их сделают

    def get_comment_review(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title=title)
        return review

    def get_queryset(self):
        review = self.get_comment_review()
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = self.get_comment_review()
        serializer.save(author=self.request.user, review=review)
