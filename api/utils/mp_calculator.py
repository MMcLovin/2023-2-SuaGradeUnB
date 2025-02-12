from typing import TypedDict

class DisciplineMP(TypedDict):
    """
    TypedDict que define uma disciplina.
    
    Attributes:
        grade: a menção obtida pelo aluno na disciplina.
        number_of_credits: a quantidade de créditos que a disciplina tem.
    """
    grade: str
    number_of_credits: int
    modulo_integrante: bool


class MpCalculator:
    """
    Classe que calcula a média ponderada (MP) das matérias optativas e obrigatórias.
    """
    def __init__(self) -> None:
        self.grade_map = {
            'SS': 5, 'MS': 4, 'MM': 3, 'MI': 2, 'II': 1, 'SR': 0,
        }

    def get_mp_value(self, disciplinas: list[DisciplineMP]) -> float:
        """
        Calcula a MP a partir de uma lista de disciplinas.
        """
        if not disciplinas:
            return 0.0

        numerador = 0
        denominador = 0

        for disciplina in disciplinas:
            if disciplina['modulo_integrante']:
                # Validação da menção:
                if disciplina['grade'].upper() not in self.grade_map:
                    raise ValueError(f"Menção inválida: {disciplina['grade']}")

                # Validação do número de créditos:
                if disciplina['number_of_credits'] <= 0:
                    raise ValueError(f"Número de créditos inválido: {disciplina['number_of_credits']}")

                numerador += self.grade_map[disciplina['grade'].upper()] * disciplina['number_of_credits']
                denominador += disciplina['number_of_credits']

        if denominador == 0:
            return 0.0
        return float(numerador / denominador)