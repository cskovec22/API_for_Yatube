from django.urls import include, path
from rest_framework import routers

from api.views import (
    CommentViewSet,
    FollowViewSet,
    # FollowList,
    GroupViewSet,
    PostViewSet
)


app_name = 'api'

router = routers.DefaultRouter()
router.register('follow', FollowViewSet, basename='follow')
# router.register(
#     r'follow',
#     FollowList,
#     basename='following'
# )
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(r'groups', GroupViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    # path('v1/follow/', FollowList.as_view()),
    path('v1/', include(router.urls)),
]
