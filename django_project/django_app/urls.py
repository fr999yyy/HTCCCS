from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #root url
    path('stdLogin', views.stdLogin, name='stdLogin'),
    path('vLogin', views.vLogin, name='vLogin'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/update', views.update, name='update'),
    path('dashboard/newYear', views.newYear, name='newYear'),
    path('dashboard/result', views.result, name='result'),
    path('upload_zip', views.upload_zip, name='upload_zip'),
    path('pSel', views.pSel, name='pSel'),
    path('pSel/check_decision', views.check_decision, name='check_decision'),
    path('stdLogout', views.stdLogout, name='stdLogout'),
]