from django.urls import path  
from . import views  

urlpatterns = [  
    path('homepage/', views.Homepage, name='homepage'),   
    path('train-model/', views.TrainModel, name='TrainModel'),  # التأكد من وجود مسار للرابط  
    path('train-model2/', views.TrainModel2 , name='TrainModel2'),  # التأكد من وجود مسار للرابط  
    path('using-model/', views.UsingModel, name='UsingModel'),  # التأكد من وجود مسار للرابط  
    path('using-model2/', views.UsingModel2, name='UsingModel2'),  # التأكد من وجود مسار للرابط  
    # path('using-model2/', views.TrainModel, name='UsingModel2'),  # التأكد من وجود مسار للرابط  
]