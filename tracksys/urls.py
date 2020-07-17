from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import settings

app_name = "tracksys"
urlpatterns = [
    path('', views.indexView, name='index'),
    path('login/', views.UserLogin, name='login'),
    path('main/', views.main, name='main'),
    path('manager/', views.managerView, name='manager'),
    path('peopleAdmin/', views.peopleAdminView, name='peopleAdmin'),
    path('certAdmin/', views.certificateAdminView, name='certAdmin'),
    path('logout/', views.user_logout, name='logout'),
    path('users/<str:cid>', views.user_view, name='user_view'),
    path('managerTree/', views.get_subordinate, name='managerTree'),
    path('tracking/', views.trackReport, name='tracking'),
    path('downloadReport/', views.downloadReport, name='download'),
    path('analyseReport/', views.analyseReport, name='analyse'),
    path('addCertPage/', views.get_add_certificate_record_page, name='addCertPage'),
    path('addCertificateRecord/', views.add_certificate_record, name='addCertificateRecord'),
    path('certAjax/', views.get_certificate_name, name='certAjax'),
    path('editCertPage/<str:cid>', views.get_edit_certificate_record_page, name='editCertPage'),
    path('updateCertificateRecord/', views.edit_certificate_record, name='updateCertificateRecord'),
    path('deleteCertificateRecord/<str:cid>', views.delete_certificate_record, name='deleteCertificateRecord'),
    path('viewCertRecordDetail/<str:cid>', views.view_certificate_detail, name='viewCertRecordDetail'),
    path('certAdminPage/', views.get_cert_admin_page, name='certAdminPage'),
    path('cert_type/',views.cert_type, name='cert_type'),
    path('add_cert_info_page/', views.add_cert_info_page,  name='add_cert_info_page'),
    path('addCertInfo/', views.add_cert_info, name='addCertInfo'),
    path('details/',views.groupSummary, name='details'),
    path('editCertPageAdmin/<str:cid>', views.edit_cert_info_page, name='editCertPageAdmin'),
    path('editCert/', views.edit_cert_info, name='editCert'),
    path('addAdmin',views.addAdminPage, name='addAdmin')

]
urlpatterns += static('/viewCertRecordDetail/', document_root=settings.UPLOADFILES_ROOT)