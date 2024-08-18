from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.

    
class Authentication(APIView):
    
    def post(self,request):
        
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
        
    def get(self,request):
        
        
        try:
            
            data = request.data
            
            serializer = CustomTokenSerializer(data=data)
            if serializer.is_valid():
                return Response({'success' : "successfully signin your account",'Token' : serializer.validated_data},status=status.HTTP_200_OK)
            else:
                return Response({'error' : serializer.errors})
            
        except Exception as e:
            return Response({'error': f'error {e}'})
        
        