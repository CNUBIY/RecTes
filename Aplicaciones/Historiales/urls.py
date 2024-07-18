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
    path('doc_inicio/doc_patient/<int:idPat>/edit_patient/', views.edit_patient, name='edit_patient'),
    path('historiales/add_alergias/<int:idPat>/', views.add_alergias, name='add_alergias'),
    #CREAR PACIENTE
    path('doc_inicio/new_patient/', views.new_patient, name='new_patient'),
    #CREAR Madre
    path('doc_inicio/doc_patient/<int:idPat>/agg_rep/', views.agg_rep, name='agg_rep'),
    path('doc_inicio/doc_patient/<int:idPat>/agg_mom/', views.agg_mom, name='agg_mom'),
    path('doc_inicio/doc_patient/<int:idPat>/agg_dad/', views.agg_dad, name='agg_dad'),
    path('doc_inicio/doc_patient/<int:idPat>/agg_mompat/', views.agg_mompat, name='agg_mompat'),
    path('doc_inicio/doc_patient/<int:idPat>/agg_dadpat/', views.agg_dadpat, name='agg_dadpat'),
]
