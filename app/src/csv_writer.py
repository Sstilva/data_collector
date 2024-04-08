import csv

from .base_writer import BaseWriter


class CSVWriter(BaseWriter):
    def __init__(self, config: dict, path: str):
        super().__init__(config)
        self.path = path
        file_header = [
            'ID',
            'Datetime',

            'Rooms', 'Address', 

            'M_Aviastroitelnaya', 'M_Severny Vokzal',
            'M_Yashlek', 'M_Kozya Sloboda',
            'M_Kremlyovskaya', 'M_Ploshchad Tukaya',
            'M_Sukonnaya Sloboda', 'M_Ametyevo',
            'M_Gorki', 'M_Prospekt Pobedy',
            'M_Dubravnaya',

            'Total Area', 'Living Area',
            'Kitchen Area', 'Floor',
            'Construction Year', 'Completion Year',
            'Building', 'Finishing',

            'Desc',

            'Type of Housing', 'Bathroom',
            'Ceilings', 'Balcony/Loggia',
            'Windows View', 'Renovation',
            'Construction Series', 'Elevators Count',
            'Construction Type', 'Flooring type',
            'Parking', 'Entrances',
            'Heating', 'Building AR',

            'Price',

            'Builder-Premium', 'Builder',
            'Agent', 'Agency', 'Homeowner',

            'URL'
        ]
        self.init_header(file_header)

    def init_header(self, file_header: list):
        '''Creates file and writes header line to it.'''
        with open(f"{self.path}.csv", 'w', newline='') as f:
            row_writer = csv.writer(f, delimiter=',')
            row_writer.writerow(file_header)

    def save_offer(self, offer: list, link: str):
        '''Appends list of values to the file.'''
        values = self._format_data(offer, link)

        with open(f"{self.path}.csv", 'a', newline='') as f:
            row_writer = csv.writer(f, delimiter=',')
            row_writer.writerow(values)

