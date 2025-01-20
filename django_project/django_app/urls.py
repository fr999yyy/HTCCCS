from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #root url
    path('stdLogin', views.stdLogin, name='stdLogin'),
    path('csLogin', views.csLogin, name='csLogin'),
    path('vLogin', views.vLogin, name='vLogin'),
    path('logout', views.logout, name='logout'),
    path('volunteer_dashboard', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/updateData', views.updateData, name='updateData'),
    path('process_excel_form', views.process_excel_form, name='process_excel_form'),
    path('courses_lookup', views.courses_lookup, name='courses_lookup'),
    path('dashboard/selection_lookup', views.selection_lookup, name='selection_lookup'),
    path('dashboard/change_results', views.change_results, name='change_results'),
    path('dashboard/upload_result_change', views.upload_result_change, name='upload_result_change'),
    path('dashboard/result', views.result, name='result'),
    path('dashboard/result/print_results_table', views.print_results_table, name='print_results_table'),
    path('dashboard/result/generate_xlsx', views.generate_xlsx, name='generate_xlsx'),
    path('truncate_data', views.truncate_data, name='truncate_data'),
    path('dashboard/result/process_selection_results', views.process_selection_results, name='process_selection_results'),
    path('upload_zip', views.upload_zip, name='upload_zip'),
    path('update_settings', views.update_settings, name='update_settings'),
    path('std_index', views.std_index, name='std_index'),
    path('pSel/<int:form_stage>', views.pSel, name='pSel'),
    path('get_courses/', views.get_courses, name='get_courses'),
    path('pSel/double_check', views.double_check, name='double_check'),
    path('pSel/confirm', views.confirm, name='confirm'),
    path('pSel/confirm/submit_form', views.submit_form, name='submit_form'),
    path('success', views.success, name='success'),
    path('stdLogout', views.stdLogout, name='stdLogout'),
]