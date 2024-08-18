
from django.urls import path
from Authentication_app.views import *

urlpatterns = [
  
  path('signup/',Signup,name='signup'),
  
  
]
