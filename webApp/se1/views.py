from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
	return render(request,'home.html',{'name':'himmi'})
	# return HttpResponse("hello world")


@csrf_exempt
def add(request):
	num1=int(request.GET["num1"])
	num2=int(request.GET["num2"])
	res=num1+num2
	return render(request,'res.html',{'result':res})
