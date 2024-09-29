from django.shortcuts import render,HttpResponse
from django.conf import settings
import sys
import os
sys.path.append(str(settings.BASE_DIR))
from Script import script
import threading
import asyncio
from django.http import JsonResponse


# from django.views import View

# Create your views here.
    
    

async def DataExtract(request):
    keyword = request.GET.get('keyword', '')
    keyword = "water"
    DE = script.DataExtract 
    print("okay")
    tasks = [
        DE.thulo_extract(keyword),
        DE.okdam_extraction(keyword),
        DE.hamro_bazar_extract(keyword),
        DE.dealayo_extraction(keyword),
        DE.daraz_extract(keyword),
    ]
    print("starting")
    results = await asyncio.gather(*tasks)
    print("done")
    return JsonResponse({
        'result1': results[0],
        'result2': results[1],
        'result3': results[2],
        'result4': results[3],
        'result5': results[4]
    })
