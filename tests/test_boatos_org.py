import unittest
import re

from scrappers.boatos_org import scrape_page

def trim(text):
    return re.sub('\s|\n|\t', '', text)

class BoatosOrgTestCase(unittest.TestCase):
    def test_page_with_red_text(self):
        self.maxDiff = None

        result = scrape_page(
            "http://www.boatos.org/saude/enfermeira-vacina-febre-amarela-farsa.html")
        expected = "Relato de uma enfermeira que pensa. “Deixem-me dizer o que eu penso sobre esse tal “surto” de febre amarela. Estudei enfermagem há quase 20 anos e na literatura sempre falou que :“a forma grave da febre amarela é raríssima.” Trabalho há 17 anos em dois dos maiores hospitais de Belo Horizonte. Não me lembro, em todos esses anos, de um só paciente internado pela forma grave da doença. Pergunto: que história é essa de “surto” de febre amarela, na forma grave, pelo país??? Porque ninguém fala sobre o que aconteceu para que a forma rara se tornasse tão ‘popular’? Eu faço minhas conclusões: primeiro, não acredito nas estatísticas divulgadas pela mídia.Segundo, não confio no treinamento e cartilhas dadas as médicos,que lhes confere como fechar o diagnóstico. “A febre amarela é uma doença infecciosa, causada por vírus e transmitida por vetores. Geralmente, quem contrai este vírus não chega a apresentar sintomas ou os mesmos são muito fracos. As primeiras manifestações da doença são repentinas: febre alta, calafrios, cansaço, dor de cabeça, dor muscular, náuseas e vômitos por cerca de três dias. A forma mais grave da doença é rara e costuma aparecer após um breve período de bem-estar (até dois dias), quando podem ocorrer insuficiências hepática erenal, icterícia (olhos e pele amarelados), manifestações hemorrágicas e cansaço intenso....Está acontecendo uma campanha no Brasil, pois o Governo está com estoque alto e não quer ter prejuízo se a validade vencer, jogar fora sai mais caro que vacinar o povo pelos exigências de descarte adequado para não contaminar o meio ambiente.Também tem os lucro$ obtidos da BigPharma se bater a meta... Negócios, sempre negócios!!! Esta vacina não é segura,alguns meses atrás houve alerta para suspender, agora estão fazendo terror no povo de novo falando que encontraram macacos mortos pra lá e pra cá... Não tomem!!!..."

        self.assertEqual(trim(result), trim(expected))
