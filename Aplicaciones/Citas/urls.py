from django.urls import path
from . import views

urlpatterns=[
    #INDEX
    path('',views.index),
    #PERFIL USUARIOS
    path('usci_inicio/',views.usci_inicio),
    #PERFIL ADMIN
    path('adci_inicio/',views.adci_inicio),
    #HORARIOS ADMIN
    path('adci_fechacitas/',views.adci_fechacitas),
    path('aggagenda_adci/',views.aggagenda_adci),
    path('adci_fechacitas/procesarActualizacionHorario/<int:id>/', views.procesarActualizacionHorario, name='procesarActualizacionHorario'),
    #DIAS ADMIN
    path('adci_dias/',views.adci_dias),
    path('agg_adci/',views.agg_adci),
    path('del_adci/<id>',views.del_adci),
]
