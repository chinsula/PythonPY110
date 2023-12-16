from django.http import JsonResponse
from store.models import DATABASE
from django.http import HttpResponse


def products_view(request):
    if request.method == "GET":
        id_product = request.GET.get('id')
        if id_product in DATABASE:
            return JsonResponse(DATABASE[id_product], json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
        if not id_product in DATABASE:
            return JsonResponse(DATABASE[id_product], json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})

        return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})# Вернуть JsonResponse с объектом DATABASE и параметрами отступов и кодировок,
def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()
        return HttpResponse(data)