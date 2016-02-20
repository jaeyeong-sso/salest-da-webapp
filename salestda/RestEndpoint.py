from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from salestda.models import HdfsClusterInfo

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class HdfsClusterInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HdfsClusterInfo
        fields = ('id', 'configured_capacity', 'present_capacity', 'dfs_used')
        
class HdfsClusterInfoVewSet(viewsets.ModelViewSet):
    queryset = HdfsClusterInfo.objects.all()
    serializer_class = HdfsClusterInfoSerializer

