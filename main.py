import requests
from bs4 import BeautifulSoup
import tabulate
#conectando ao site fonte
headers={'User-Agent':'Mozilla/5.0'}
resposta=requests.get('https://www.fundamentus.com.br/fii_resultado.php',headers=headers)
#fazendo o parcer do conteudo da pagina
soup= BeautifulSoup(resposta.text,'html.parser')
print(soup.prettify())
#recolhendo as informaçoes das linhas da tabela
linhas=soup.find(id='tabelaResultado').find('tbody').find_all('tr')

for linha in linhas:
  dados_fundo=linha.find_all('td')
  print(f'[{dados_fundo[0].text}]\nCotação:{dados_fundo[2].text}\nSetor:{dados_fundo[1].text}\nDY %{dados_fundo[4].text}\nP/Pv:{dados_fundo[5].text}\n')

pass

