from django.urls import path, re_path

from images import views

app_name = 'images'
urlpatterns = [
    path('create/', views.image_create, name='create'),
    re_path(r'^detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.image_detail, name='detail'),
]
