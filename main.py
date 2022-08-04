import requests
from bs4 import BeautifulSoup
import locale

from modelos import FundoImobiliario, Estrategia
from tabulate import tabulate

locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')

def trata_porcentagem(porcentagem_str):
  return locale.atof(porcentagem_str.split('%')[0])
def trata_decimal(decimal_str):
  return locale.atof(decimal_str)

#conectando ao site fonte
headers={'User-Agent':'Mozilla/5.0'}
resposta=requests.get('https://www.fundamentus.com.br/fii_resultado.php',headers=headers)
#fazendo o parcer do conteudo da pagina
soup= BeautifulSoup(resposta.text,'html.parser')

#recolhendo as informaçoes das linhas da tabela
linhas=soup.find(id='tabelaResultado').find('tbody').find_all('tr')
resultado=[]
estrategia=Estrategia(cotacao_atual_minima=50.0,
                      divident_yield_minimo=5,
                      p_vp_minimo=0.70,
                      valor_mercado_minimo=200000000,
                      liquidez_minimo=50000,
                      qt_minimo_imovel=5,
                      maxima_vacancia_media=10)
for linha in linhas:


  dados_fundo=linha.find_all('td')
  codigo=dados_fundo[0].text
  segmento=dados_fundo[1].text
  cotacao_atual=trata_decimal(dados_fundo[2].text)
  ffo_yield=trata_porcentagem(dados_fundo[3].text)
  divident_yield=trata_porcentagem(dados_fundo[4].text)
  p_vp=trata_decimal(dados_fundo[5].text)
  valor_mercado=trata_decimal(dados_fundo[6].text)
  liquidez=trata_decimal(dados_fundo[7].text)
  qt_imovel=int(dados_fundo[8].text)
  preco_m2=trata_decimal(dados_fundo[9].text)
  aluguel_m2=trata_decimal(dados_fundo[10].text)
  cap_rate=trata_porcentagem(dados_fundo[11].text)
  vacancia_media=trata_porcentagem(dados_fundo[12].text)
#criação do modelo de fundo imobiliario


  fundo_imobiliario=FundoImobiliario(codigo,segmento,cotacao_atual,ffo_yield,
                 divident_yield,p_vp,valor_mercado,liquidez,qt_imovel,
                 preco_m2,aluguel_m2,cap_rate,vacancia_media)

  if estrategia.aplica_estrategia(fundo_imobiliario):
    resultado.append(fundo_imobiliario)


cabecalho=["Codigo","Segmento","Cotação Atual","Divident Yield"]
tabela=[]
for elemento in resultado:
    tabela.append([elemento.codigo,elemento.segmento,locale.currency(elemento.cotacao_atual),
                   f'{locale.str(elemento.divident_yield)} %',
                   ])

print(tabulate(tabela,headers=cabecalho,showindex='always',tablefmt='fancy_grid'))

