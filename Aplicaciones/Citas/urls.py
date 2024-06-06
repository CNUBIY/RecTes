from django.urls import path
from . import views


urlpatterns=[
    #INDEX
    path('',views.index),
    #LOGIN USUARIOS
    path('usci_login/',views.usci_login),
    #REGISTER USUARIOS
    path('usci_reg/',views.usci_reg),
    path('usci_addreg/',views.usci_addreg),
    path('check-email/', views.check_email_exists, name='check_email_exists'),
    #GENERAL USUARIO
    path('usci_inicio/',views.usci_inicio, name='usci_inicio'),
    #PERIL USUARIO
    path('usci_perfil/',views.usci_perfil),
    #PERFIL ADMIN
    path('adci_perfil/',views.adci_perfil),
    #GENERAL ADMIN
    path('adci_inicio/',views.adci_inicio),
    path('adci_inicio/aggin_adci/',views.aggin_adci),
    path('adci_inicio/procesarActualizacionHorarioIn/<int:id>/', views.procesarActualizacionHorarioIn, name='procesarActualizacionHorarioIn'),
    path('delete_adciIn/<id>/',views.delete_adciIn),
    #CONTABILIDAD
    path('adci_inicio/cont_inicio/', views.cont_inicio),
    path('adci_inicio/cont_inicio/cont_int/',views.cont_int),
    path('adci_inicio/addcont_adci/<id>',views.addcont_adci, name='addcont_adci'),
    path('adci_inicio/aggcont_adci/', views.aggcont_adci, name='aggcont_adci'),
    #HORARIOS ADMIN
    path('adci_fechacitas/',views.adci_fechacitas),
    path('aggagenda_adci/',views.aggagenda_adci),
    path('delete_adci/<id>',views.delete_adci),
    path('adci_fechacitas/procesarActualizacionHorario/<int:id>/', views.procesarActualizacionHorario, name='procesarActualizacionHorario'),
    #ERRORES
    path('error_p/',views.error_p),
]
