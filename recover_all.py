from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import re
import os


def uf_all_month(year):
    #url cambia segun ano
    base_url = "http://www.sii.cl/valores_y_fechas/uf/uf"+str(year)+".htm"
    #se abre la url
    driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver')
    driver.get(base_url)  
    #retorna un obj de todo lo que hay en table export
    meses = driver.find_element_by_id('table_export')
    months = []
    #busca todos los tr dentro de meses
    for mes in meses.find_elements_by_xpath("//tr"):
        #si esque la tr esta vacia o esta el nombre del mes no la agrega
        if(mes.text != '' and mes.text.find('Ene') == -1):
            # al tener vacios entremedio, se necesitan eliminar los vacios que se originan al tener 
            # distintos largo los meses, por lo que se eliminar los espacios en blanco
            m = mes.text.split(' ')
            if(len(m) > 15):
                if(m[15] == ''):
                    m.pop(15)
                if(m[12] == ''):
                    m.pop(12)
                if(m[8] == ''):
                    m.pop(8)
                if(m[5] == ''):
                    m.pop(5)
            if(m[2] == ''):
                m.pop(2)
            months.append(m)
    #se cierra la url (pantalla)
    driver.close()
    return months
