from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import operator

def uf(number_month):
    base_url = 'http://www.sii.cl/valores_y_fechas/uf/uf2020.htm'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    m = uf_month(number_month)
    if(m != 0):
        table = soup.find('div',m) #retorna el div, correspondiente al mes.
        tr = table.find_all('tr')
        days = []
        values = []
        for row in tr:
            days.append(row.find_all('th')) # captura todos los th (donde estan los dias)
        for row in tr:
            values.append(row.find_all('td')) # captura todos los td (donde estan los valores)
        informacion = {} #objeto que guardara todos los datos
        dias = []
        valores = []
        #recorre y saca el arreglo de los dias
        for i in range (1,len(days)):
            for j in range (0,len(days[i])):
                aux = days[i][j].text.replace('<th width="40"><strong>','').replace('</strong></th>','')
                dias.append(aux)
        #recorre y saca el arreglo de valores de uf
        for i in range (0,len(values)):
            for j in range (0,len(values[i])):
                aux = values[i][j].text.replace('<td width="200">','').replace('</td>','')
                valores.append(aux)
        html = ''
        #rellena el dicc. final
        for i in range (0,len(dias)):
            if(dias[i] != '' and valores[i] != ''):
                informacion[dias[i]] = valores[i]
        informacion = (sorted(informacion.items(),key=operator.itemgetter(1)))
        for inf in informacion:
            html += '<p>' + inf[0] + ': ' + inf[1] + '</p>'
        return informacion
    else:
        return []

def uf_html():
    all_uf = uf()
    html = ''
    for inf in all_uf:
        html += '<p>' + inf[0] + ': ' + inf[1] + '</p>'
    return html

def uf_month(argument): 
    argument = int(argument)
    switcher = { 
        1: {'id':'mes_enero'}, 
        2: {'id':'mes_febrero'}, 
        3: {'id':'mes_marzo'},
    } 
  
    return switcher.get(argument, 0) 
  