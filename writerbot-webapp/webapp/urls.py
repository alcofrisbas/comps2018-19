from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('write/', views.write),
    path('about/', views.about),
    path('team/', views.team),
    path('logout/', views.logout),
    path('saves/',views.saves),
    path('new_story', views.newStory),
    path('load_story/<str:title>', views.loadStory),
    path('delete_story/<str:title>', views.deleteStory)
]
