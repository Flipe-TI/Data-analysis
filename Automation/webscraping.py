import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import datetime as dt

def data():
    # get na data de hoje
    today = dt.date.today()


    # o sitema só da valores do proximo dia util na tabela, considerando que domingo seria um dia util
    if today.weekday() == 5:# se o dia da semana for sexta ele vai adicionar mais dois dias na data
        proximo_dia_util = today + dt.timedelta(days = 2)
    else:# caso contrario ele retornar o proximo dia util
        proximo_dia_util = today + dt.timedelta(days = 1)

    # aqui transformo a data em texto
    data_txt = proximo_dia_util.strftime('%d/%m/%Y')

    return data_txt

#path
PATH = "C:\Program Files (x86)\chromedriver.exe"

#---------------------------------------------------------------------------------------
# aqui eu oculto todo o processo de automação e inicio o mesmo
option = Options()
option.headless = True

driver = webdriver.Chrome(PATH)

driver.get("https://www.csonline.com.br/pt-BR/Pages/Login/Login.aspx")
time.sleep(2)
#---------------------------------------------------------------------------------------
# aqui fica a automação do login
# seleciono as box para login
username = driver.find_element_by_id("signInName")
username.clear()
username.send_keys("")# entre os parênteses coloque o login

password = driver.find_element_by_id("password")
password.clear()
password.send_keys("")# e entre esses parênteses a senha

driver.find_element_by_id("next").click() #click no botão de acesso
time.sleep(8) # tempo de espera para que a pagina carregue
driver.find_element_by_id("btnSelectLogin").click()# segunda tela de seleção
time.sleep(8)# tempo de espera para que a pagina carregue
#---------------------------------------------------------------------------------------
# aqui vou diretamente para a seção no site odne fica a tabela de preços e já começo o tratamento para levar ao PowerBI
driver.get("https://www.csonline.com.br/pt-BR/spa/index.aspx#!/price")# ir para a pagina que possui os preços

time.sleep(8)# tempo de carregamento novamente


Tabela_html = driver.find_element_by_tag_name("table")# seleciona a tabela pelo name table


html_content = Tabela_html.get_attribute('outerHTML')# retira todos os atributos da pagina em HTML
soup =BeautifulSoup(html_content,'html.parser') # aqui criamos uma arvore para ser analisada e posteriormente extrairmos os dados
table =soup.find(name='table') #selecionamos aquilo que está na tabela

# a biblioteca panda agora fica responsavel pelo tratamento dos dados
df_full = pd.read_html(str(table))[0]# aqui lemos os codigos em html e transformamos em string o que está no table
df = df_full[['Produto', 'Preço para entrega (CIF)data'.replace('data',data())]]# retiramos somente as colunas citadas
df.columns = ['Produto', 'Preço']# renomeio as colunas
print(df)


driver.quit()