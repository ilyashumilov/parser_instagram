from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
from .parser import parser

@api_view(['GET'])
def main(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        data = parser().get(username)
        print(data)
        return Response(data)