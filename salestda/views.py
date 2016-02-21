from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from salestda.models import HdfsClusterInfo
from RestEndpoint import HdfsClusterInfoSerializer
from rest_framework.renderers import JSONRenderer

from rest_framework import status
import PandasAnalysis as pa

@api_view(['GET'])
def get_monthly_sales_volumn_data(request):
    if request.method == 'GET':
        #hdfslusterInfo = HdfsClusterInfo.objects.get(pk=1)
        #serializer = HdfsClusterInfoSerializer(hdfslusterInfo)
        
        list_df = pa.agg_montly_sales_volumn()
        content = JSONRenderer().render(list_df)
        return Response(content, status=status.HTTP_200_OK)


def index(request):
    return render(request, 'salestda/index.html')

