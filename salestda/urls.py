from django.conf.urls import url, include

from . import views

from RestEndpoint import UserViewSet
from RestEndpoint import HdfsClusterInfoVewSet

from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'_hdfsClusterInfo',HdfsClusterInfoVewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] 

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)