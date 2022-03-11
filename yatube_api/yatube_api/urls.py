from rest_framework import routers

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/posts', PostViewSet)
router.register(r'api/v1/groups', GroupViewSet)
router.register(r'api/v1/follow', FollowViewSet, basename='follow')
router.register(r'api/v1/posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/v1/', include('djoser.urls.jwt')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
