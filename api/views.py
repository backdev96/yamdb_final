from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import CustomUserSerializer
from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import (IsAdminOrReadOnly, IsAuthorOrAdminOrModerator,
                          IsSuperUser)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    '''Category view. Display Category model. Admin only permission.'''
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def retrieve(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    '''Genre view. Display Genre model. Admin only permission.'''
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def retrieve(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserMeViewSet(generics.RetrieveUpdateAPIView):
    '''UserMe view. Custom user serializer.'''
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


class TitleViewSet(viewsets.ModelViewSet):
    '''Title view. Display Tittle model. Title filter.'''
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsSuperUser]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    '''Review view. Staff or Author permission.'''
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        title = Title.objects.get(pk=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def rating_calc(self, title):
        '''Rating calculation function.'''
        reviews = Review.objects.filter(title=title)
        rating_average = reviews.aggregate(Avg('score'))['score__avg']
        title.rating = rating_average
        title.save()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        self.rating_calc(title)

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        self.rating_calc(title)


class CommentViewSet(viewsets.ModelViewSet):
    '''Comment view. Comment Serializer. Pagination.'''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get("title_id"))
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, review=review)
