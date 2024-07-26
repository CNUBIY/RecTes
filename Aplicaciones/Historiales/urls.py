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
    path('doc_inicio/doc_patient/<int:idPat>/edit_mom/',views.edit_mom, name='edit_mom'),
    path('doc_inicio/doc_patient/<int:idPat>/edit_dad/',views.edit_dad, name='edit_dad'),
    path('doc_inicio/doc_patient/<int:idPat>/agg_infomom', views.agg_infomom, name='agg_infomom'),
    path('doc_inicio/doc_patient/<int:idPat>/agg_obs', views.agg_obs, name='agg_obs'),
    path('doc_inicio/doc_patient/<int:idPat>/pagosMama', views.pagosMama, name='pagosMama'),
    path('doc_inicio/doc_patient/<int:idPat>/pagosPapa', views.pagosPapa, name='pagosPapa'),
    path('doc_inicio/doc_patient/<int:idPat>/editPagosMama', views.editPagosMama, name='editPagosMama'),
    path('doc_inicio/doc_patient/<int:idPat>/editPagosPapa', views.editPagosPapa, name='editPagosPapa'),
    path('historiales/doc_inicio/doc_patient/<int:idPat>/edit_infomom/<int:id>/', views.edit_infomom, name='edit_infomom'),
    path('historiales/add_alergias/<int:idPat>/', views.add_alergias, name='add_alergias'),
    path('historiales/delete_alergia/<int:idPat>/<int:alergia_id>/', views.delete_alergia, name='delete_alergia'),
    #CREAR PACIENTE
    path('doc_inicio/new_patient/', views.new_patient, name='new_patient'),
    #CREAR Madre
    path('doc_inicio/doc_patient/<int:idPat>/agg_rep/', views.agg_rep, name='agg_rep'),
    path('doc_inicio/doc_patient/<int:idPat>/agg_mom/', views.agg_mom, name='agg_mom'),
    path('doc_inicio/doc_patient/<int:idPat>/agg_dad/', views.agg_dad, name='agg_dad'),
    path('doc_inicio/doc_patient/<int:idPat>/agg_mompat/', views.agg_mompat, name='agg_mompat'),
    path('doc_inicio/doc_patient/<int:idPat>/agg_dadpat/', views.agg_dadpat, name='agg_dadpat'),

    #ESTATURAS PADRE Y MADRE
    path('doc_inicio/doc_patient/<int:idPat>/aggEstatura', views.aggEstatura, name='aggEstatura'),

    #OBSERVACIONES
    path('doc_inicio/viewobs/<int:id>/', views.viewobs, name='viewobs'),
    path('doc_inicio/viewobs/<int:id>/edit_obs', views.edit_obs, name='edit_obs'),

    #DIAGNOSTICOS
    path('doc_inicio/viewobs/<int:id>/addDiagnostico',views.addDiagnostico,name='addDiagnostico'),
    path('doc_inicio/viewobs/<int:id>/editDiagnostico', views.editDiagnostico, name='editDiagnostico'),

    #RECETAS
    path('doc_inicio/viewobs/<int:id>/addReceta', views.addReceta, name='addReceta'),
    path('doc_inicio/viewobs/<int:idobs>/edit_receta/<int:idreceta>/', views.editReceta, name='editReceta'),
    path('historiales/doc_inicio/viewobs/<int:idobs>/deleteReceta/<int:idReceta>/', views.deleteReceta, name='deleteReceta'),

    #ALERGIAS
    path('doc_inicio/alergias/',views.alergias, name='alergias'),
    path('doc_inicio/newalergia/',views.newalergia, name='newalergia'),
    path('doc_inicio/deleteAlergia/<int:id>',views.deleteAlergia, name='deleteAlergia'),
    path('doc_inicio/editAlergia/<int:id>',views.editAlergia, name='editAlergia'),


    #CIE10
    path('doc_inicio/reportcie', views.reportcie, name='reportcie'),
    path('doc_inicio/newcie', views.newcie, name='newcie'),
    path('doc_inicio/deletecie/<int:id>',views.deletecie, name='deletecie'),
    path('doc_inicio/editcie/<int:id>', views.editcie, name='editcie'),


    #MEDICAMENTOS
    path('doc_inicio/medicamentos', views.medicamentos, name='medicamentos'),
    path('doc_inicio/newMedicina', views.newMedicina, name='newMedicina'),
    path('doc_inicio/deleteMedicina/<int:id>',views.deleteMedicina, name='deleteMedicina'),
    path('doc_inicio/editMedicina/<int:id>/', views.editMedicina, name='editMedicina'),

    #REPRESENTANTES
    path('doc_inicio/representantesLista/', views.representantesLista, name='representantesLista'),
    path('doc_inicio/editMadre/<int:id>/', views.editMadre, name='editMadre'),
    path('doc_inicio/editPadre/<int:id>/', views.editPadre, name='editPadre'),
    path('doc_inicio/aggMom/', views.aggMom, name='aggMom'),
    path('doc_inicio/aggDad/', views.aggDad, name='aggDad'),
    path('doc_inicio/deleteMadre/<int:id>/', views.deleteMadre, name='deleteMadre'),
    path('doc_inicio/deletePadre/<int:id>/', views.deletePadre, name='deletePadre'),
]
