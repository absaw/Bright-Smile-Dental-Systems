from django.shortcuts import render

# Create your views here.

def get_index(request):
    if request.method == "GET":
        return render(request,'index_hello.html')