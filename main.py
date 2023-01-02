from collections import namedtuple
from datetime import datetime

import math
import pytz
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

file = open("RU.txt", "r", encoding="utf8")
geo_object_list = file.readlines()
file.close()
# объявление именованного кортежа, который соответствует набору данных
geo_objects_tuple = namedtuple('GeoObject',
                               'GeonameId,Name,AsciiName,AlternateNames,Latitude,Longitude,FeatureClass,FeatureCode,'
                               'CountryCode,Cc2,Admin1Code,Admin2Code,Admin3Code,Admin4Code,Population,Elevation,Dem,'
                               'Timezone,ModificationDate')

# список из именованных кортежей, который содержит информацию о городах
geo_objects = [geo_objects_tuple(*geo_object.strip().split("\t")) for geo_object in geo_object_list]

max_number = 100  # предполагаем, что максимальное количество городов на странице равняется 100
max_page = math.ceil(len(geo_objects) / max_number)  # максимальное количество страниц
print(max_page)
max_page_max_number = len(geo_objects) % max_number  # максимальное количество городов на последней странице


@app.errorhandler(404)  # обработчик ошибки, если будет обращение по несуществующему маршруту
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/get_by_id/<int:town_id>', methods=["GET"])
def town_info(town_id):
    for geo_object in geo_objects:
        if int(geo_object.GeonameId) == town_id:
            return jsonify({"town": geo_object._asdict()})
    return make_response(jsonify({'error': 'Not found'}), 404)  # если города не было найдено


@app.route('/api/towns_info/<town1>/<town2>', methods=["GET"])
def towns_info(town1, town2):
    found_town1 = None
    found_town2 = None
    for geo_object in geo_objects:
        # если указанный город (на русском) присутствует в списке альтернативных названий города
        if town1 in geo_object.AlternateNames.split(","):
            if found_town1 is None:
                found_town1 = geo_object
            # проверка на разницу в населении, если город с таким названием попадается не в первый раз
            elif int(found_town1.Population) < int(geo_object.Population):
                found_town1 = geo_object
        if town2 in geo_object.AlternateNames.split(","):
            if found_town2 is None:
                found_town2 = geo_object
            elif int(found_town2.Population) < int(geo_object.Population):
                found_town2 = geo_object
    if found_town1 is None or found_town2 is None:  # проверка на существование введенных городов
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        is_similar_timezone = False
        to_the_north = 'the same longitude'
        time_zone_difference = 0
        if found_town1.Timezone == found_town2.Timezone:  # проверка на временные зоны
            is_similar_timezone = True
        else:
            town1_tz = pytz.timezone(found_town1.Timezone)
            town2_tz = pytz.timezone(found_town2.Timezone)
            dt = datetime.now()
            date_with_tz_1 = town1_tz.localize(dt)
            date_with_tz_2 = town2_tz.localize(dt)
            time_zone_difference = date_with_tz_1 - date_with_tz_2
        # проверки на широту, чем она больше, тем севернее
        if float(found_town1.Latitude) > float(found_town2.Latitude):
            to_the_north = found_town1.Name
        elif float(found_town1.Latitude) < float(found_town2.Latitude):
            to_the_north = found_town2.Name
        return jsonify({"town1": found_town1._asdict(), "town2": found_town2._asdict(),
                        'toTheNorth': to_the_north, 'isSimilarTimezone': is_similar_timezone,
                        'timeZoneDifference': str(time_zone_difference)})


@app.route('/api/towns_clue/<town1>', methods=["GET"])
def town_clue(town1):
    similar_towns = list()
    for geo_object in geo_objects:
        if town1 in geo_object.AlternateNames:  # если введенная часть города есть в строке альтернативных названий
            for alternate_town in geo_object.AlternateNames.split(','):  # проход по циклу их альтернативных названий
                if town1 in alternate_town:  # если введенная часть города есть в строке альтернативного названия
                    similar_towns.append(alternate_town)  # считаем, что название города подходит под подсказку
    if len(similar_towns) == 0:  # если похожих городов не было найдено
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({"towns": similar_towns})


""""
Более эффективное решение, т.к генератор будет быстрее, однако менее читаемое. Решил взять более читаемый вариант
new_sim = [alter_town for geo_object in geo_objects if town1 in geo_object.AlternateNames for alter_town in geo_object.AlternateNames.split(',') if town1 in alter_town]
"""


@app.route('/towns_list/<int:page>/<int:number>', methods=["GET"])
def towns_list(page, number):
    if page < max_page:
        if number <= max_number:
            start_towns = (page - 1) * max_number  # если страница = 1 , то срез начинается с 0, если 2, то со 100 и т.д
            stop_towns = (page - 1) * max_number + number  # если страница = 1, то срез оканчивается на 0 + число и т.д
            geo_objects_seq = [geo_object._asdict() for geo_object in geo_objects[start_towns:stop_towns]]
            return jsonify({"towns": geo_objects_seq})
        else:
            return make_response(jsonify({'error': 'Not found'}), 404)
    elif page == max_page:  # убедиться, что реально входит в максимум, а не за один шаг до него
        if number <= max_page_max_number:
            start_towns = (max_page - 1) * max_number
            stop_towns = (max_page - 1) * max_number + number
            geo_objects_seq = [geo_object._asdict() for geo_object in geo_objects[start_towns:stop_towns]]
            return jsonify({"towns": geo_objects_seq})
        else:
            return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
