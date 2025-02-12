from django.test import TestCase
from api.utils.mp_calculator import MpCalculator, DisciplineMP  

class TestMpCalculator(TestCase):

    def test_get_mp_value_lista_vazia(self):
        calculadora = MpCalculator()
        disciplinas: list[DisciplineMP] = []
        resultado = calculadora.get_mp_value(disciplinas)
        self.assertEqual(resultado, 0.0)

    def test_get_mp_value_uma_disciplina(self):
        calculadora = MpCalculator()
        disciplina: DisciplineMP = {'grade': 'SS', 'number_of_credits': 4, 'modulo_integrante': True} 
        resultado = calculadora.get_mp_value([disciplina])  
        self.assertEqual(resultado, 5.0)

    def test_get_mp_value_uma_disciplina_nao_integrante(self):
        calculadora = MpCalculator()
        disciplina: DisciplineMP = {'grade': 'SS', 'number_of_credits': 4, 'modulo_integrante': False} 
        resultado = calculadora.get_mp_value([disciplina])  
        self.assertEqual(resultado, 0.0)
          
    def test_get_mp_value_multiplas_disciplinas(self):
        calculadora = MpCalculator()
        disciplinas: list[DisciplineMP] = [
            {'grade': 'SS', 'number_of_credits': 4, 'modulo_integrante': True},
            {'grade': 'MS', 'number_of_credits': 2, 'modulo_integrante': True},
            {'grade': 'II', 'number_of_credits': 3, 'modulo_integrante': False}, 
            {'grade': 'MM', 'number_of_credits': 1, 'modulo_integrante': True},
        ]
        # Cálculo manual da MP esperada:
        # MP = ((5 * 4) + (4 * 2) + (3 * 1)) / (4 + 2 + 1) = 4.4286
        resultado = calculadora.get_mp_value(disciplinas)
        self.assertAlmostEqual(resultado, 4.4286, places=4)  

    def test_get_mp_value_mencao_invalida(self):
        calculadora = MpCalculator()
        disciplinas: list[DisciplineMP] = [
            {'grade': 'XX', 'number_of_credits': 4, 'modulo_integrante': True}
        ]
        with self.assertRaises(ValueError): 
            calculadora.get_mp_value(disciplinas)

    def test_get_mp_value_creditos_invalidos(self):
        calculadora = MpCalculator()
        disciplinas: list[DisciplineMP] = [
            {'grade': 'SS', 'number_of_credits': 0, 'modulo_integrante': True}  
        ]
        with self.assertRaises(ValueError):  
            calculadora.get_mp_value(disciplinas)

        disciplinas2: list[DisciplineMP] = [
            {'grade': 'SS', 'number_of_credits': -1, 'modulo_integrante': True}  
        ]
        with self.assertRaises(ValueError):
            calculadora.get_mp_value(disciplinas2)

