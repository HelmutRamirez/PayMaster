from django.shortcuts import render 

def homePrincipal(request): 
     return render(request,'home.html')
