from django.urls import path
from . import views
# from .views import DiaHorarioList

urlpatterns=[
    #INDEX
    path('',views.index),
    #PERFIL USUARIOS
    path('usci_login/',views.usci_login),
    path('usci_inicio/',views.usci_inicio),
    path('usci_perfil/',views.usci_perfil),
    #PERFIL ADMIN
    path('adci_perfil/',views.adci_perfil),
    #GENERAL ADMIN
    path('adci_inicio/',views.adci_inicio),
    #path('api/horarios/', DiaHorarioList.as_view(), name='api_horarios'),
    #HORARIOS ADMIN
    path('adci_fechacitas/',views.adci_fechacitas),
    path('aggagenda_adci/',views.aggagenda_adci),
    path('delete_adci/<id>',views.delete_adci),
    path('aggsem_adci/',views.aggsem_adci, name='aggsem_adci'),
    path('adci_fechacitas/procesarActualizacionHorario/<int:id>/', views.procesarActualizacionHorario, name='procesarActualizacionHorario'),

]
