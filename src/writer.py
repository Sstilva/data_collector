from datetime import datetime 
import csv


class Writer(object):
    def __init__(self, file_header: list, path: str):
        self.date_today = datetime.today().strftime('%Y-%m-%d')
        self.path = path
        self.init_header(file_header)

        self.stations = [
            'Авиастроительная', 'Северный вокзал',
            'Яшьлек', 'Козья слобода',
            'Кремлёвская', 'Площадь Габдуллы Тукая',
            'Суконная слобода', 'Аметьево',
            'Горки', 'Проспект Победы',
            'Дубравная'
        ]
        self.factoids = [
            'Общая площадь', 'Жилая площадь',
            'Площадь кухни', 'Этаж',
            'Год постройки', 'Год сдачи',
            'Дом', 'Отделка'
        ]
        self.summary = [
            'Тип жилья', 'Санузел',
            'Высота потолков', 'Балкон/лоджия',
            'Вид из окон', 'Ремонт', 
            'Строительная серия', 'Количество лифтов',
            'Тип дома', 'Тип перекрытий',
            'Парковка', 'Подъезды',
            'Отопление', 'Аварийность'
        ]
        self.sellers = [
            'Агентство недвижимости', 'Застройщик', 
            'Риелтор', 'Собственник'
        ]

    def init_header(self, file_header: list):
        with open(f"{self.path}_{self.date_today}.csv", 'w', newline='') as csv_file:
            row_writer = csv.writer(csv_file, delimiter=',')
            row_writer.writerow(file_header)

    def save_to_file(self, offer: dict):
        concat_values = [x for xs in self._format_data(offer) for x in xs]

        with open(f"{self.path}_{self.date_today}.csv", 'a', newline='') as csv_file:
            row_writer = csv.writer(csv_file, delimiter=',')
            row_writer.writerow(concat_values)

    def _format_data(self, offer: dict) -> list:
        data = [
                self._form_title(offer['title']), 
                self._form_address(offer['address']),
                self._form_dict(self.stations, offer['underground'], ' мин.'),
                self._form_dict(self.factoids, offer['factoids'], '\xa0м²'),
                self._form_dict(self.summary, offer['summary'], '\xa0м'),
                self._skip_form(offer['price']),
                self._form_seller(self.sellers, list(offer.items())[-4:])
        ]

        return data

    _form_title = lambda self, x: list([x[0]])
    _form_address = lambda self, x: list([' '.join(x)])
    _skip_form = lambda self, x: list([x])

    @staticmethod
    def _form_dict(headers: list, raw: dict, rm_sub: str) -> list:
        clean = []

        for _ in headers:
            if _ in raw.keys():
                clean.append(raw[_].replace(rm_sub, ''))
            else:
                clean.append(None)

        return clean

    @staticmethod
    def _form_seller(headers: list, raw: list) -> list:
        clean = []
        stop = False

        for seller in raw:
            if (type(seller[1]) is not list) and (not stop):
                for _ in headers:
                    if _ in seller[1].keys():
                        clean.append(seller[1][_])
                        stop = True
                    else:
                        clean.append(None)

        return clean

