from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from datetime import datetime, timedelta, time
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from collections import defaultdict
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.decorators import method_decorator
from Aplicaciones.Citas.middleware import login_required as custom_login_required
# Create your views here.



@login_required
def doc_inicio (request):
    return render(request,'general/doc_inicio.html')
