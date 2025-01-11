from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #root url
    path('stdLogin', views.stdLogin, name='stdLogin'),
    path('vLogin', views.vLogin, name='vLogin'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/updateData', views.updateData, name='updateData'),
    path('process_excel_form', views.process_excel_form, name='process_excel_form'),
    path('dashboard/result', views.result, name='result'),
    path('dashboard/result/print_results_table', views.print_results_table, name='print_results_table'),
    path('dashboard/result/check_priority', views.check_priority, name='check_priority'),
    path('truncate_data', views.truncate_data, name='truncate_data'),
    path('dashboard/result/process_selection_results', views.process_selection_results, name='process_selection_results'),
    path('upload_zip', views.upload_zip, name='upload_zip'),
    path('update_settings', views.update_settings, name='update_settings'),
    path('pSel', views.pSel, name='pSel'),
    path('get_courses/', views.get_courses, name='get_courses'),
    path('pSel/double_check', views.double_check, name='double_check'),
    path('pSel/confirm', views.confirm, name='confirm'),
    path('pSel/confirm/submit_form', views.submit_form, name='submit_form'),
    path('success', views.success, name='success'),
    path('stdLogout', views.stdLogout, name='stdLogout'),
]