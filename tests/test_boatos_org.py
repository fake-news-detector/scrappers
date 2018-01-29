import unittest
import requests

from scrappers.boatos_org import scrape_page
from tests.helpers import trim, load_fixture
from unittest.mock import MagicMock
from collections import namedtuple


def scrape_mocked(fixture_file, url):
    fixture = load_fixture("boatos_org", fixture_file, url)
    MockedRequest = namedtuple('MockedRequest', 'text')
    original_get = requests.get

    requests.get = MagicMock(return_value=MockedRequest(text=fixture))
    result = scrape_page(url)
    requests.get = original_get

    return result

class BoatosOrgTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.maxDiff = None

    def test_page_with_red_text(self):
        result = scrape_mocked(
            "red_text.html",
            "http://www.boatos.org/saude/enfermeira-vacina-febre-amarela-farsa.html"
        )
        expected = "Relato de uma enfermeira que pensa.  “Deixem-me dizer o que eu penso sobre essetal “surto” de febre amarela. Estudei enfermagem há quase 20 anos e na literatura sempre falou que : “a forma grave da febre amarela é raríssima.” Trabalho há 17 anos em dois dos maiores hospitais de Belo Horizonte. Não me lembro, em todosesses anos, de um só paciente internado pela forma grave da doença. Pergunto: que história é essa de “surto” de febre amarela, na forma grave, pelo país??? Porque ninguém fala sobre o que aconteceu para que a forma rara se tornasse tão ‘popular’? Eu faço minhas conclusões: primeiro, não acredito nas estatísticas divulgadas pela mídia. Segundo, não confio no treinamento e cartilhas dadas as médicos, que lhes confere como fechar o diagnóstico. “A febre amarela é uma doença infecciosa, causada por vírus e transmitida por vetores. Geralmente, quem contrai este vírus não chega a apresentar sintomas ou os mesmos são muito fracos. As primeiras manifestações da doença são repentinas: febre alta, calafrios, cansaço, dor de cabeça, dor muscular, náuseas e vômitos por cerca de três dias. A forma mais grave da doença é rara e costuma aparecer após um breve período de bem-estar (até dois dias), quando podem ocorrer insuficiências hepática e renal, icterícia (olhos e pele amarelados), manifestações hemorrágicas e cansaço intenso. ... Está acontecendo uma campanha no Brasil, pois o Governo está com estoque alto e nãoquer ter prejuízo se a validade vencer, jogar fora sai mais caro que vacinar o povo pelos exigências de descarte adequado para não contaminar o meio ambiente. Também tem os lucro$ obtidos da BigPharma se bater a meta... Negócios, sempre negócios!!!  Esta vacina não é segura, alguns meses atrás houve alerta para suspender, agora estão fazendo terror no povo de novo falando que encontraram macacos mortos pra lá e pra cá... Não tomem!!!..."

        self.assertEqual(trim(result), trim(expected))

    def test_page_with_italic_text(self):
        result = scrape_mocked(
            "italic_text.html",
            "http://www.boatos.org/politica/crivella-fechar-sao-cristovao.html"
        )
        expected = "Crivella vai fechar a Feira de São Cristóvão no Rio de Janeiro, diz boato A Riotur, em conjunto com os órgãos públicos competentes, realizou fiscalizações no Centro Luiz Gonzaga de Tradições Nordestinas e encontrou irregularidades, tais como falta de prestação de contas legítima e eleições transparentes, não pagamentodas tarifas públicas e desrespeito às posturas municipais da lei no 2.052/1993.As incorreções também fazem parte do Inquérito Civil do Ministério Público do Rio de Janeiro (2016.01137017), em notificação enviada à Riotur, solicitando a intervenção da Empresa de Turismo na gestão direta do Pavilhão de São Cristóvão.  Tais incorreções ferem o contrato firmado entre a Prefeitura do Rio, através da Riotur, que em outubro de 2018 assumiu as atribuições relativas à administração,supervisão e coordenação, e a Associação de Feirantes do Centro Luiz Gonzaga deTradições Nordestinas. Tais argumentos corroboram a ação de rescindir o contrato entre as partes, conforme publicado em 26/01/2018 no Diário Oficial do Município do Rio de Janeiro.  Na segunda-feira (29), será publicada no DO uma portaria instituindo uma Comissão Eleitoral para fins de formação da nova Comissão de Organização e Administração do Centro Municipal Luiz Gonzaga de Tradições Nordestinas, com um prazo estipulado de 45 dias para eleições do novo Conselho Orientador, formado e eleito pelos próprios feirantes. Durante este período, a Riotur continuará executando seu trabalho de administração do Pavilhão, através de seus servidores, garantindo o pleno funcionamento deste importante espaço cultural e de interesse turístico da cidade do Rio de Janeiro."

        self.assertEqual(trim(result), trim(expected))

    def test_page_with_multiple_texts(self):
        result = scrape_mocked(
            "multiple_texts.html",
            "http://www.boatos.org/politica/teori-zavascki-foi-assassinado.html"
        )
        expected = "Mataram o relator da Lava Jato no STF Teori iria homologar a delação da Odebrecht em poucos dias.  Somente uma intervenção militar nos salvará dos corruptos. ... Relator da Lava Jato foi assassinado assim como Eduardo Campos O ministro Teori Zavascki iria homologar em poucos dias a delação da Odebrecht. Não ha dúvidasque ele foi assassinado, assim como Eduardo Campos. No Brasil, quando alguém ameaça os planos dos corruptos, sempre há um avião que cai. ... Sem palavras para expressar o que estou sentindo. O ministro Teori lavou a alma do STF à frente daLava-Jato, surpreendeu a todos pelo extremo zelo com que suportou todo esse período conturbado. Agora, na véspera da homologação da colaboração premiada da Odebrecht, esse ‘acidente’ deve ser investigado a fundo. É óbvio que há movimentos dos mais variados tipos para frear a Lava Jato. Penso que é até infantil que nãohá, isto é, que criminosos do pior tipo (conforme MPF afirma) simplesmente resolveram se submeter à lei! Acredito que a Lei e as instituições vão vencer. Porém, alerto: se algo acontecer com alguém da minha família, vocês já sabem onde procurar...! Fica o recado!"

        self.assertEqual(trim(result), trim(expected))

    def test_returns_none_for_no_text(self):
        result = scrape_mocked(
            "no_text.html",
            "http://www.boatos.org/saude/matar-macacos-febre-amarela-humanos.html"
        )

        self.assertEqual(result, None)
