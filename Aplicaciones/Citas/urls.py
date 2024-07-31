from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns=[
    #INDEX
    path('',views.index, name='index'),
    #LOGIN ADMIN
    path('register/', views.register, name='register'),
    path('verify/',views.verify_email, name='verify'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    #PERFIL ADMIN
    path('adci_inicio/adci_perfil/', views.adci_perfil, name='adci_perfil'),
    path('adci_inicio/adci_perfil/del_us/<user_id>',views.eliminar_usuario, name='eliminar_usuario'),
    path('adci_inicio/adci_perfil/promote_user_to_admin/', views.promote_user_to_admin, name='promote_user_to_admin'),
    path('adci_inicio/adci_perfil/delete_account/', views.delete_account, name='delete_account'),
    #GENERAL ADMIN
    path('adci_inicio/',views.adci_inicio, name='adci_inicio'),
    path('adci_inicio/aggin_adci/',views.aggin_adci),
    path('adci_inicio/procesarActualizacionHorarioIn/<int:id>/', views.procesarActualizacionHorarioIn, name='procesarActualizacionHorarioIn'),
    path('delete_adciIn/<id>/',views.delete_adciIn),
    #PAGOSREALIZADOS
    path('adci_inicio/cont_inicio/', views.cont_inicio),
    path('adci_inicio/cont_inicio/cont_int/',views.cont_int, name='cont_int'),
    path('adci_inicio/addcont_adci/<id>',views.addcont_adci, name='addcont_adci'),
    path('adci_inicio/aggcont_adci/', views.aggcont_adci, name='aggcont_adci'),

    #HORARIOS ADMIN
    path('adci_fechacitas/',views.adci_fechacitas),
    path('verificar_cita/', views.verificar_cita, name='verificar_cita'),
    path('aggagenda_adci/',views.aggagenda_adci),
    path('delete_adci/<id>',views.delete_adci),
    path('adci_fechacitas/procesarActualizacionHorario/<int:id>/', views.procesarActualizacionHorario, name='procesarActualizacionHorario'),
    path('check_appointment/', views.check_appointment, name='check_appointment'),
    #ERRORES
    path('error_p/',views.error_p, name='error_p'),
]
