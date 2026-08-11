from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('found_items/',views.found, name='found_items'),
    path('lost_items/',views.lost, name='lost_items'),
    path('detect-item/',views.detect, name='detect_item'),
]
