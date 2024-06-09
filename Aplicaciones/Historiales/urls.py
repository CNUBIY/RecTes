from django.urls import path
from . import views

urlpatterns=[
    path('doc_inicio/', views.doc_inicio, name='doc_inicio')
]
