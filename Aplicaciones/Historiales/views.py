from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def doc_inicio (request):
    return render(request,'general/doc_inicio.html')
