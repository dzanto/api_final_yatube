from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('group', views.GroupViewSet)
router.register('follow', views.FollowViewSet)
router.register(r'posts/(?P<post_id>[0-9]+)/comments', views.CommentViewSet, basename='CommentViewSet')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
