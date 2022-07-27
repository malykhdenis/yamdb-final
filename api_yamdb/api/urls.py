from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)
from users.views import UserRegViewSet, UserViewSet, RegAPIView

app_name = 'api'

router = routers.DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('users', UserViewSet)
router.register(r'titles/(?P<id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(r'titles/\d+/reviews/(?P<id>\d+)/comments', CommentViewSet,
                basename='comments')
router.register('auth/signup', UserRegViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', RegAPIView.as_view(), name='token_obtain'),
]
