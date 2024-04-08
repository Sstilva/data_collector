from datetime import datetime


class BaseWriter(object):
    def __init__(self, config: dict):
        self.stations = config['underground']
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
            'Агентство', 'Риелтор', 'Собственник'
        ]

    def _format_data(self, offer: list, link: str) -> list:
        '''Formats parts of offer using unique methods for each and
        concatenates them all into one list.'''
        data = [
            self._form_id(link),
            self._form_timestamp,
            self._form_title(offer[0]), 
            self._form_address(offer[1]),
            self._form_dict(self.stations, offer[2], ' мин.'),
            self._form_dict(self.factoids, offer[3], '\xa0м²'),
            self._skip_form(offer[4]),
            self._form_dict(self.summary, offer[5], '\xa0м'),
            self._skip_form(offer[6]),
            self._form_seller(self.sellers, offer[-4:])
        ]
        values = [x for xs in data for x in xs]
        values.append(link)

        return values

    _form_id = lambda self, x: list([x.split('/')[-2]]) 
    _form_timestamp = list([datetime.today().strftime(r'%Y-%m-%d %H:%M:%S')])
    _form_title = lambda self, x: list([x[0]])
    _form_address = lambda self, x: list([' '.join(x)])
    _skip_form = lambda self, x: list([x])

    @staticmethod
    def _form_dict(headers: list, raw: dict, rm_sub: str) -> list:
        clean = []

        for _ in headers:
            if _ in raw.keys():
                clean.append(raw[_].replace(',', '.').replace(rm_sub, ''))
            else:
                clean.append(None)

        return clean

    @staticmethod
    def _form_seller(headers: list, raw: list) -> list:
        clean = []
        stop = False

        for seller in raw:
            if (seller) and (not stop):
                for _ in headers:
                    if _ in seller.keys():
                        clean.append(seller[_])
                        stop = True
                    else:
                        clean.append(None)

        return clean

