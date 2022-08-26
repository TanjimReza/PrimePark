"""PrimePark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from home import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('createslot/', views.createslot, name='createslot'),
    path('table/', views.table, name='table'),
    path('drivers/', views.drivers, name='drivers'),
    path('driverdashboard/', views.driverdashboard, name='driverdashboard'),
    path('reviews/<str:id>/', views.reviews, name='reviews'),
    path('reviews/', views.reviews, name='reviews'),
    path('allreviews/', views.allreviews, name='allreviews'),
    path('bookslot/<str:id>/', views.bookslot, name='bookslot'),

   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)