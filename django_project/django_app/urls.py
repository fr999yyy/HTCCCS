from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #root url
    path('stdLogin', views.stdLogin, name='stdLogin'),
    path('vLogin', views.vLogin, name='vLogin'),
    path('pSel', views.pSel, name='pSel'),
]