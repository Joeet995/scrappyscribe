from django.urls import path
from . import views

# This is a namespace for our app's URLs
app_name = 'transcriber'

urlpatterns = [
    # path('url_pattern/', view_function, name='url_name')
    path('', views.upload_audio, name='upload_audio'),
    path('file/<int:pk>/', views.audiofile_detail, name='audiofile_detail'),
]