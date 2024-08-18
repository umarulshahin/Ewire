from Authentication_app.models import *
from .models import *
from rest_framework import serializers



class PostSerializer(serializers.ModelSerializer):
     
    class Meta:
       model = Post
       fields = ['id', 'user', 'title', 'description', 'publish']
    
    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        print(instance,'yes working')
        print(validated_data,'yes coming')
        
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.publish = validated_data.get('publish', instance.publish)
        instance.save()
        return instance
    
class TaguserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User_Tag
        fields = [ 'users', 'post']
 
