from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
from .parser import inst_parser

@api_view(['GET'])
def main(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        data = inst_parser().get_page(username)
        print(data)
        return Response(data)