
from django.urls import path
from Authentication_app.views import *
from User_app.views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    
  path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
  
  path('Authentication/',Authentication.as_view(),name='Authentication'),
  
  path('userpost/',UserPost.as_view(),name='userpost'),
  
  path('postlike/',PostLIkeView.as_view(),name='postlike'),
  

]
