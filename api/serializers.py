from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    '''Serializer for Category model'''

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    '''Serializer for Genre model'''

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategoryReprField(serializers.SlugRelatedField):
    '''Serializer for Category model'''

    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}


class GenreReprField(serializers.SlugRelatedField):
    '''GenreReprField Serializer'''

    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}


class TitleSerializer(serializers.ModelSerializer):
    '''Serializer for Title model.'''
    category = CategoryReprField(slug_field='slug',
                                 queryset=Category.objects.all())
    genre = GenreReprField(slug_field='slug',
                           queryset=Genre.objects.all(),
                           many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    '''Serializer for Review model. Slug related field author.'''
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def get_serializer_context(self):
        return {'title_id': self.kwargs['title_id'], 'request': self.request}

    def validate(self, data):
        '''Call the instance's validate() method and
        raise error if user has already added a review for this tittle.
        '''
        title_id = self.context.get('request').parser_context['kwargs']['title_id']
        if (Review.objects.filter(title_id=title_id, author=self.context['request'].user).exists()
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError('This user has already added review for this title')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    '''Serializer for Comment model. Slug related field author.'''
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class EmailSerializer(serializers.Serializer):
    '''Email Serializer'''
    email = serializers.EmailField(required=True)
