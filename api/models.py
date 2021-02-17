from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser


class Category(models.Model):
    '''Category model. Ordered by name.'''
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Genre(models.Model):
    '''Genre model. Ordered by name.'''
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Title(models.Model):
    '''Title model. Related to Genre and Category models, ordered by name.'''
    name = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField()
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True, verbose_name='Категория'
    )
    rating = models.IntegerField(blank=True, null=True, verbose_name='Рейтинг')
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Review(models.Model):
    '''Review model. Related to Tittle and Author models, ordered by pub_date.'''
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    score = models.PositiveSmallIntegerField(
        default=0, validators=(MinValueValidator(1, message='Value should be greater than 1'),
                               MaxValueValidator(10, message='Value should be less than 10')),
        verbose_name='Рейтинг')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('pub_date',)


class Comment(models.Model):
    '''Comment model. Related to Review and Author models, ordered by pub_date.'''
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('pub_date',)
