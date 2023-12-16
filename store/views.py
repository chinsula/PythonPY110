from django.http import JsonResponse
from store.models import DATABASE
from django.http import HttpResponse


def products_view(request):
    if request.method == "GET":

        return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})# Вернуть JsonResponse с объектом DATABASE и параметрами отступов и кодировок,
def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()
        return HttpResponse(data)