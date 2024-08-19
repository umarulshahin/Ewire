from Authentication_app.models import *
from .models import *
from rest_framework import serializers



class PostSerializer(serializers.ModelSerializer):
    Like_count = serializers.SerializerMethodField()
    class Meta:
       model = Post
       fields = ['id', 'user', 'title', 'description', 'publish', 'save_date', 'Like_count']
    
    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.publish = validated_data.get('publish', instance.publish)
        instance.save()
        return instance
    
    def get_Like_count(self,obj):
        
        return Like.objects.filter(post=obj.id).count()
     
class TaguserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User_Tag
        fields = [ 'users', 'post']
 
class PostLikeSerializer(serializers.ModelSerializer):
    
    Like_count = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['users', 'post' , 'Like_count']
        
    def get_Like_count(self,obj):
        
         return Like.objects.filter(post=obj.post).count()