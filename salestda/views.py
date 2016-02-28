from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from salestda.models import HdfsClusterInfo
from RestEndpoint import HdfsClusterInfoSerializer
from rest_framework.renderers import JSONRenderer

from rest_framework import status
import PandasAnalysis as pa

from rest_framework import serializers

class SerPostRequestParam(serializers.Serializer):
    category = serializers.CharField()
    def getCategory(self):
        return self.category
    

@api_view(['GET'])
def get_monthly_sales_volumn_data(request):
    if request.method == 'GET':
        #hdfslusterInfo = HdfsClusterInfo.objects.get(pk=1)
        #serializer = HdfsClusterInfoSerializer(hdfslusterInfo)
        
        list_df = pa.agg_montly_sales_volumn(1,10000)
        content = JSONRenderer().render(list_df)
        return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_desc_total_sales_volumn(request):
    if request.method == 'GET':
        desc_dict = pa.desc_total_sales_volumn()
        content = JSONRenderer().render(desc_dict)
        return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_monthly_total_amount_per_product_cate(request):
    if request.method == 'GET':
        dictData = pa.agg_montly_total_amount_by_product_cate()
        content = JSONRenderer().render(dictData)
        return Response(content, status=status.HTTP_200_OK)

@api_view(['POST'])
@parser_classes((JSONParser,))
def get_monthly_total_amount_product_cate_detail(request,format=None):
    if request.method == 'POST':
        cateReqParam = request.data['category']
        dictData = pa.agg_montly_total_amount_by_product(cateReqParam)       
        content = JSONRenderer().render(dictData)
        return Response(content, status=status.HTTP_200_OK)
    
def index(request):
    return render(request, 'salestda/index.html')

