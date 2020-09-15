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
router.register(r'posts/(?P<post_id>[0-9]+)/comments', views.CommentAPI, basename='CommentViewSet')

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/group/', views.GroupAPIView.as_view()),
    path('v1/follow/', views.FollowAPIView.as_view()),
    path('v1/', include(router.urls)),
]
