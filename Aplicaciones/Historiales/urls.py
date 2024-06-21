from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    #LOGIN DOCTOR
    path('logindoc/', views.user_login, name='logindoc'),
    path('logoutdoc/',views.user_logout, name='logoutdoc'),
    #GENERAL DOCTOR
    path('doc_inicio/', views.doc_inicio, name='doc_inicio'),
    #HISTORIALES DOCTOR
    path('doc_inicio/doc_patient/<idPat>', views.doc_patient, name='doc_patient'),
    #CREAR PACIENTE
    path('doc_inicio/new_patient/', views.new_patient, name='new_patient'),
]
