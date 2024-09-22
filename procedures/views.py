# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Procedure

@login_required
def procedure_list(request):
    procedures = Procedure.objects.all()
    data = [{'id': procedure.id, 'name': procedure.name} for procedure in procedures]
    # print('procedures::',data) #Verified
    return JsonResponse(data, safe=False)