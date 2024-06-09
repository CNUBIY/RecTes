from django.shortcuts import render, redirect

# Create your views here.
def doc_inicio (request):
    return render(request,'general/doc_inicio.html')
