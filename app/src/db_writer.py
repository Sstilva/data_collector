from datetime import datetime
import psycopg

from .base_writer import BaseWriter


class DBWriter(BaseWriter):
    def __init__(self, config: dict):
        super().__init__(config)
        self.db_con_str = 'dbname=CianDatabase user=yurt'

    def save_offer(self, offer: list, link: str):
        '''Connects to PostgreSQL database via psycopg3, executes INSERT query.'''
        values = self._format_data(offer, link)
        # Remove datetime from values list because PostgreSQL have it's own timestamp.
        values.pop(1)

        with psycopg.connect(self.db_con_str) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        """INSERT INTO offers (
                            id, rooms, address, 
                            m_aviastroitelnaya, m_severny_vokzal, m_yashlek,
                            m_kozya_sloboda, m_kremlyovskaya, m_ploshchad_tukaya,
                            m_sukonnaya_sloboda, m_ametyevo, m_gorki,
                            m_prospekt_pobedy, m_dubravnaya,
                            total_area, living_area, kitchen_area,
                            floor, construction_year, completion_year,
                            building, finishing, description, type_of_housing,
                            bathroom, ceilings, balcony_loggia, window_view,
                            renovation, construction_series,
                            elevator_count, construction_type,
                            flooring_type, parking, entrances, heating, building_ar,
                            price, builder_premium, builder, agent, agency, homeowner,
                            url
                        ) VALUES ( 
                            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                        )""", (values)
                    )

                except psycopg.errors.UniqueViolation:
                    conn.rollback()

                else:
                    conn.commit()

                finally:
                    conn.close()

