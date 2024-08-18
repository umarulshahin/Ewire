from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import *
from Authentication_app.models import *
    
class UserPost(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self,request):
        
        data = request.data
        user = request.user
        
        try:
            
            data['user'] = user.id
            serializer = PostSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                post_id = serializer.data['id']
                print(post_id)
                
                if data['tag']:
                    
                    for user in data['tag']:
                        try:
                            values=CustomUser.objects.get(Username=user)
                            tagData={
                                "users" : values.id,
                                "post": post_id
                            }
                            
                            print(tagData)
                            
                            tagSerializer = TaguserSerializer(data=tagData)   
                            
                            if tagSerializer.is_valid():
                                tagSerializer.save()
                                print(tagSerializer.data)
                                
                            else:
                                return Response({'error' : tagSerializer.errors})
                                
                        except CustomUser.DoesNotExist:
                            
                            return Response({'error': f'User with username {user} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

                       
                    return Response ({'success':tagSerializer.data},status=status.HTTP_201_CREATED)
                return Response ({'success':serializer.data},status=status.HTTP_201_CREATED)
            
            return Response({'error':serializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            
            return Response(f"error occured {e}")
        
    def patch(self,request):
        
        data = request.data
        try:
            
          post = Post.objects.get(pk=data['id'])
          
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response({'success' : "post update successfully",'data' : serializer.data },status=status.HTTP_200_OK)
        
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
                
