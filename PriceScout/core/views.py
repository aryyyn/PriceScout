from django.shortcuts import render,HttpResponse
from django.conf import settings
import sys
import os
sys.path.append(str(settings.BASE_DIR))
from Script import script
import threading
import asyncio
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status


# from django.views import View

# Create your views here.
    
    

async def home(request):
    if request.method == "POST":
        try: 
            keyword = request.POST.get("textbox")
            DE = script.DataExtract 
            tasks = [
                DE.thulo_extract(keyword),
                DE.okdam_extraction(keyword),
                DE.hamro_bazar_extract(keyword),
                DE.dealayo_extraction(keyword),
                DE.daraz_extract(keyword),
            ]
            results = await asyncio.gather(*tasks)
            context =  {
                'Thulo': results[0],
                'OkDam': results[1],
                'Hamro Bazaar': results[2],
                'Dealayo': results[3],
                'Daraz': results[4]
            }
            return render(request, "home.html", context={'context': context})
        except Exception as err:
            print("Error:", err)
            return render(request, "home.html", context={'error': str(err)})
    
    return render(request, "home.html")

# class Home():
#     async def home(self,request):
#         if request.method == 'POST':
#             ItemName = request.POST.get("textbox")
#             print(ItemName)
        
#         return render(request, "home.html")