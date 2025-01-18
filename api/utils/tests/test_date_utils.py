from rest_framework.test import APITestCase
from utils import sessions as sns
from datetime import datetime


class DateUtilsTest(APITestCase):

    def compare_date(self, date: datetime):
        before_dec = datetime(date.year + 1, 1, 1) >= date
        after_may = datetime(date.year, 5, 2) <= date

        return before_dec and after_may

    def change_date(self, date: datetime):
        month = 2 if self.compare_date(date) else 6
        return datetime(date.year + self.compare_date(date), month=month, day=1)

    def test_get_current_year_and_period_with_right_may_limits(self):
        year, period = sns.get_current_year_and_period(datetime(2023, 5, 1))

        self.assertEqual("2023", year)
        self.assertEqual("1", period)

        year, period = sns.get_current_year_and_period(datetime(2023, 5, 2))

        self.assertEqual("2023", year)
        self.assertEqual("2", period)
    
    def test_get_current_year_and_period_with_left_jan_limits(self):
        year, period = sns.get_current_year_and_period(datetime(2023, 12, 31))

        self.assertEqual("2023", year)
        self.assertEqual("2", period)

        year, period = sns.get_current_year_and_period(datetime(2024, 1, 1))

        self.assertEqual("2024", year)
        self.assertEqual("1", period)
    
    def test_get_current_year_and_period_with_middle_date(self):
        year, period = sns.get_current_year_and_period(datetime(2023, 2, 18))

        self.assertEqual("2023", year)
        self.assertEqual("1", period)

        year, period = sns.get_current_year_and_period(datetime(2023, 9, 20))

        self.assertEqual("2023", year)
        self.assertEqual("2", period)

        year, period = sns.get_current_year_and_period(datetime(2024, 4, 23))

        self.assertEqual("2024", year)
        self.assertEqual("1", period)

        year, period = sns.get_current_year_and_period(datetime(2024, 7, 9))

        self.assertEqual("2024", year)
        self.assertEqual("2", period)

    def test_get_next_period(self):
        _, period = sns.get_next_period()

        date = datetime.now()
        self.assertEqual((period == '2'), not self.compare_date(date))
        self.assertEqual((period == '1'), self.compare_date(date))

        date = self.change_date(date)
        _, period = sns.get_next_period(date)

        self.assertEqual((period == '2'), not self.compare_date(date))
        self.assertEqual((period == '1'), self.compare_date(date))

    def test_get_next_period_with_year(self):
        year, period = sns.get_next_period()

        date = datetime.now()
        self.assertEqual(str(date.year + (not (period == '2'))), year)

        date = self.change_date(date)
        year, period = sns.get_next_period(date)

        self.assertEqual(str(date.year + (not (period == '2'))), year)

    def test_get_previous_period(self):
        _, period = sns.get_previous_period()

        date = datetime.now()
        self.assertEqual((period == '2'), not self.compare_date(date))
        self.assertEqual((period == '1'), self.compare_date(date))

        date = self.change_date(date)
        _, period = sns.get_previous_period(date)

        self.assertEqual((period == '2'), not self.compare_date(date))
        self.assertEqual((period == '1'), self.compare_date(date))

    def test_get_previous_period_with_year(self):
        year, period = sns.get_previous_period()

        date = datetime.now()
        self.assertEqual(str(date.year - (period == '2')), year)

        date = self.change_date(date)
        year, period = sns.get_previous_period(date)

        self.assertEqual(str(date.year - (period == '2')), year)

     # D1.Condição 1 Verdadeiro
    def test_data_nula(self):
        resultado = sns.get_current_year_and_period(None)
        self.assertEqual(len(resultado), 2) 
        self.assertTrue(resultado[0].isdigit())
        self.assertEqual(resultado[1], "1")

    # D2.Condição_1 F, D2.Condição_2 V 
    def test_fora_intervalo_antes(self):
        date = datetime(2025, 4, 1)
        resultado = sns.get_current_year_and_period(date)
        self.assertEqual(resultado, ["2025", "1"])  

    # D2.Condição_1 V, D2.Condição_2 V
    def test_inicio_intervalo(self):
        date = datetime(2025, 5, 2)
        resultado = sns.get_current_year_and_period(date)
        self.assertEqual(resultado, ["2025", "2"])  

    # D2.Condição_1 V, D2.Condição_2 F
    def test_fora_intervalo_depois(self):
        date = datetime(2025, 1, 2)
        resultado = sns.get_current_year_and_period(date)
        self.assertEqual(resultado, ["2025", "1"])  