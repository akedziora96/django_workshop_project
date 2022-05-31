"""django_workshop_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from conference_room_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SearchRoom.as_view()),
    path('room/new/', views.AddRoom.as_view()),
    path('rooms/', views.DisplayRooms.as_view()),
    path('room/delete/<int:room_id>/', views.DeleteRoom.as_view()),
    path('room/modify/<int:room_id>/', views.EditRoom.as_view()),
    path('room/reserve/<int:room_id>/', views.ReserveRoom.as_view()),
    path('room/<int:room_id>/', views.RoomDetails.as_view()),
]
