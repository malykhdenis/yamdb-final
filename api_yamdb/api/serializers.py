from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Genre serializer."""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        lookup_field = 'slug'


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Title patch & post serializer."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = datetime.today().year
        if year < value:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class TitleSerializer(serializers.ModelSerializer):
    """Title serializer."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        if obj.reviews.all():
            rating = obj.reviews.aggregate(Avg('score'))
            return int(rating.get('score__avg'))
        return None


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError('Рейтинг должен быть '
                                              'от 1 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
