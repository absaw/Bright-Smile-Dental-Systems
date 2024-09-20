from django.shortcuts import render

def not_found_view(request):
    return render(request, '404.html')