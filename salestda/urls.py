from django.conf.urls import url, include

from . import views

from RestEndpoint import UserViewSet
from RestEndpoint import HdfsClusterInfoViewSet

from rest_framework import routers

from rest_framework.urlpatterns import format_suffix_patterns


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
#router.register(r'_hdfsClusterInfo',HdfsClusterInfoViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/monthly_sales_vol$', views.get_monthly_sales_volumn_data),
    #url(r'^api', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] 

urlpatterns = format_suffix_patterns(urlpatterns)

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)