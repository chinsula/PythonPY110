from django.http import JsonResponse
from store.models import DATABASE
from django.http import HttpResponse, HttpResponseNotFound


def products_view(request):
    if request.method == "GET":
        id_product = request.GET.get('id')
        if not id_product:
            return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})# Вернуть JsonResponse с объектом DATABASE и параметрами отступов и кодировок,
        if id_product in DATABASE:
            return JsonResponse(DATABASE[id_product], json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
        if id_product not in DATABASE:
            return HttpResponseNotFound("Данного продукта нет в базе данных")

def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()
        return HttpResponse(data)


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
                    with open(f'store/products/{page}.html', encoding="utf-8") as f:
                        data = f.read()
                    return HttpResponse(data)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                with open(f'store/products/{data["html"]}.html', encoding="utf-8") as f:
                    data = f.read()
                return HttpResponse(data)

        # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
        # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
        return HttpResponse(status=404)