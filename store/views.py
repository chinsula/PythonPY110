from django.http import JsonResponse
from store.models import DATABASE
from django.http import HttpResponse, HttpResponseNotFound
from logic.services import filtering_category
from logic.services import view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import render
from django.shortcuts import redirect



def products_view(request):
    if request.method == "GET":
        id_product = request.GET.get('id')
        if not id_product:
            category_key = request.GET.get("category")
            ordering_key = request.GET.get("ordering")
            reverse = request.GET.get("reverse") in ('true', 'True')
            data = filtering_category(DATABASE, category_key, ordering_key, reverse)
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

        if id_product in DATABASE:
            return JsonResponse(DATABASE[id_product], json_dumps_params={'ensure_ascii': False,
                                                                         'indent': 4})
        if id_product not in DATABASE:
            return HttpResponseNotFound("Данного продукта нет в базе данных")


def shop_view(request):
    if request.method == "GET":
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")

        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key,
                                          True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)

        return render(request, 'store/shop.html',
                      context={"products": data, "category": category_key})


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    product_category = [
                        product for product in DATABASE.values()
                        if data['category'] == product['category']
                           and product['html'] != page
                    ][:4]
                    return render(request, "store/product.html",
                                  context={"product": data, "product_category": product_category})

        elif isinstance(page, int):
            # Обрабатываем условие того, что пытаемся получить страницу товара по его id
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:
                return render(request, "store/product.html", context={"product": data})

        return HttpResponse(status=404)


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})

        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE[
                product_id]  # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
            # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            product["quantity"] = quantity
            product[
                "price_total"] = f"{quantity * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака
            # 3. добавьте product в список products
            products.append(product)

        return render(request, "store/cart.html", context={"products": products})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def coupon_check_view(request, name_coupon):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "discount": 10,
            "is_valid": True},
        "coupon_old": {
            "discount": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        if DATA_COUPON.get(name_coupon):
            return JsonResponse(DATA_COUPON.get(name_coupon),
                                json_dumps_params={'ensure_ascii': False})

        return HttpResponseNotFound("Неверный купон")

def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 80},
            "fix_price": {"price": 100},
        },
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        if DATA_PRICE.get(country):
            db_country = DATA_PRICE.get(country)
            return JsonResponse(db_country.get(city, db_country.get('fix_price')),
                                json_dumps_params={'ensure_ascii': False})

        return HttpResponseNotFound("Неверные данные")

def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")

def cart_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound("Неудачное удаление из корзины")
