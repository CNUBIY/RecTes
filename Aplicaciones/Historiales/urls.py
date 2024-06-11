from django.urls import path
from . import views

urlpatterns=[
    #LOGIN DOCTOR
    path('logindoc/', views.user_login, name='logindoc'),
    path('logoutdoc/',views.user_logout, name='logoutdoc'),
    path('doc_inicio/', views.doc_inicio, name='doc_inicio')
]
