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
        
            
    def get(self,request):
        
        posts = Post.objects.filter(publish=True).order_by('-save_date')
        serializer=PostSerializer(posts, many=True)
                    
        return Response({'success':serializer.data})

class PostLIkeView(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self,request):
        
        data = request.data
        user = request.user
        
        try:
            
           post = Post.objects.get(id=data['post'])
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if Like.objects.filter(post=post,users=user).exists():
            return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        
        postdata={
            "post":post.id,
            "users":user.id
        }
        
        serializer = PostLikeSerializer(data=postdata)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':serializer.data})
        return Response({'error' : serializer.errors})
    
    def delete(self,request):
        
        data = request.data
        user = request.user
        
        try:
            
            like = Like.objects.get(post=data['post'],users=user.id)
            post = like.post
            like.delete()
            like_count = Like.objects.filter(post=post).count()
            
            return Response({'success': 'Post unliked successfully','like_count':like_count}, status=status.HTTP_204_NO_CONTENT)
           

        except Like.DoesNotExist:
            
            return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
