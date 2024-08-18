from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from rest_framework import status

# Create your views here.

@api_view(['POST'])
def Signup(request):
    
    try:
        data = request.data
        print(data,'user datas')
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success" : "successfully account created"})
    
        return Response({'error':serializer.errors},)
    except Exception as e:
        
        print(f"Error processing request: {str(e)}")
        return Response({"error": f"An error occurred {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    