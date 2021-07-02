from django.shortcuts import render
import requests
import random
import string
import secrets
import re
import json
from django.core.cache import cache

# Create your views here.
from rest_framework import views, viewsets
from rest_framework.response import Response
from bs4 import BeautifulSoup

from django.core.exceptions import ObjectDoesNotExist, BadRequest

from .tools import get_page_tags


class LoginView(views.APIView):

    symbols_list = string.ascii_letters + string.digits

    def get(self, request):
        input_phone = request.GET.get('phone')
        if not input_phone or len(input_phone.strip()) != 11:
            raise BadRequest(
                "Не был передан 'phone' в формате '+79993322110'")
        phones = request.GET.get('phone')

        # Убираем пробел, если телефон написан с '+'
        phone = phones.strip()

        # генерирую простой код подтверждения.
        code = ''.join(random.choice(self.symbols_list)
                       for i in range(6)).upper()

        cache.set(phone, code, 600)
        return Response(code)

    def post(self, request):
        data = json.loads(request.body)
        phones = data.get('phone')
        code = data.get('code')
        if not phones or not code:
            raise BadRequest('Неверно переданы параметры "phone" или "code"')
        # if len(phones.strip()) != 11:
        #     raise BadRequest("Не был передан 'phone' в формате '+79993322110'")

        # ищу номера телефонов через регулярку.
        phones = re.findall(r'[+]\d*', phones)

        if len(phones) == 2 and phones[0] == phones[1] and len(phones[0][1:]) == 11:
            phone = phones[0][1:]
        else:
            raise BadRequest("Проверьте, правильно ли введен параметр 'phone'")
        if cache.get(phone) == code:
            return Response({'Status': 'OK'})
        else:
            return Response({"Status": 'Fail'})


class GetStructure(views.APIView):
    """
    Класс для получения всех HTML-тегов заданного сайта.
    filter_tags - теги, которые нужно вернуть в ответе.
    count_tags - количество тегов на странице.
    """

    def get(self, request):
        page = requests.get('http://freestylo.ru/')
        if request.GET.get('link'):
            page = requests.get(request.GET['link'])
        count_tags = get_page_tags(page)
        if request.GET.get('tags'):
            filter_tags = {}
            for tag in request.GET.get('tags').split(','):
                tag = tag.strip()
                filter_tags[tag] = count_tags[tag]
                result = json.dumps(filter_tags)
        else:
            result = json.dumps(count_tags)
        print(result)
        return Response(result)


class CheckStructure(views.APIView):
    """
    Класс для сравнения заданной структуры HTML-тегов с известной на сайте.
    count_tags - количество тегов на странице.
    stucture - переданное количество тегов для сравнения.
    """

    def get(self, request):
        return Response('Response for web interface')

    def post(self, request):
        data = json.loads(request.body)
        page = requests.get(data['link'])
        structure = data.get('structure')
        count_tags = get_page_tags(page)
        if structure == count_tags:
            return Response({'is_correct': True})
        else:
            difference = {}
            for key in structure.keys():
                if count_tags.get(key) != structure.get(key):
                    difference[key] = structure[key]
            return Response({"is_correct": False, 'difference': difference})
