from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from salestda.models import HdfsClusterInfo
from RestEndpoint import HdfsClusterInfoSerializer
from rest_framework.renderers import JSONRenderer

from salestda.models import MonthlyTrAgg
from RestEndpoint import MonthlyTrAggSerializer
from rest_framework import status
import PandasAnalysis as pa

@api_view(['GET', 'POST'])
def monthly_agg_report(request):
    if request.method == 'GET':
        monthlyTrAgg = MonthlyTrAgg(num_of_order=1000, total_amount=1440000)
        #hdfslusterInfo = HdfsClusterInfo.objects.get(pk=1)
        #serializer = HdfsClusterInfoSerializer(hdfslusterInfo)
        list_df = pa.aggregateMonthlyTrSummary()
        content = JSONRenderer().render(list_df)
        return Response(content, status=status.HTTP_200_OK)


def index(request):
    return render(request, 'salestda/index.html')

