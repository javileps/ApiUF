from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from recover import *
from models import *
from recover_all import *

app = Flask(__name__)
#definicion de BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/indicator_store'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def main():
    #template inicial
    return render_template('index.html')

@app.route('/rellenar/<number_month>')
def rellenar(number_month):
    #rellena por segun el numero de mes, del ano 2020! solo del 2020, utiliza beautiful soup
    #retorna los datos del mes (numero 1 = enero, 2 = febrero ....) en un object
    mes_uf = uf(number_month)
    for aux in mes_uf:
        #recorre el object, y busca si existe cada uno, si existe lo actualiza (valores), si no, agrega.
        uf_exist = UfIndicator.query.filter_by(day=aux[0],month=number_month,year=2020).first()
        if(uf_exist):
            uf_indicator = UfIndicator.query.get(uf_exist.id)
            uf_indicator.value = aux[1]
            db.session.commit()
        else:
            count = UfIndicator.query.count() + 1
            uf_indicator = UfIndicator(count,aux[0],number_month,aux[1],2020)
            db.session.add(uf_indicator)
            db.session.commit()
    
    # return render_template('rellena.html')

@app.route('/rellenar_selenium/<number_year>')
def rellenar_selenium(number_year):
    #rellena con utilizando selenium segun el anno
    #retorna los datos de todo el anno en un object
    all_months = uf_all_month(number_year)
    for mes in all_months:
        #recorre el object desde el 1, porque el primer dato son las cabeceras de la tabla (dia, enero, febrero ....)
        for i in range(1,len(mes)):
            #si exite lo actualiza, si no lo agrega
            uf_exist = UfIndicator.query.filter_by(day=mes[0],month=i,year=number_year).first()
            if(uf_exist):
                uf_indicator = UfIndicator.query.get(uf_exist.id)
                uf_indicator.value = mes[i]
                db.session.commit()
            else:
                if(mes[i]!= ''):
                    count = UfIndicator.query.count() + 1
                    uf_indicator = UfIndicator(count,mes[0],i,mes[i],number_year)
                    db.session.add(uf_indicator)
                    db.session.commit()


@app.route('/mostrar_valores/<number_month>/<year>')
def mostrar_valores(number_month,year):
    meses = ['Meses','Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'] 
    #muestra los vales segun numero de mes y anno
    #retorna todos los datos desde la BD, del mes y ano, en order asc del dia
    mes_uf = UfIndicator.query.filter_by(month=number_month,year=year).order_by(UfIndicator.day)
    #retorna numero del mes
    month = uf_month(number_month)
    #si no tiene datos ( count() = 0) llama a las funciones de agregaar, si no retonar la vista y muestra valores.
    if(mes_uf.count() == 0):
        # si es ano 2020 rellena con beautifulsoup, si no con selenium
        if(int(year) == 2020):
            rellenar (number_month)
        else:
            rellenar_selenium(year)
        mes_uf = UfIndicator.query.filter_by(month=number_month,year=year).order_by(UfIndicator.day)
        return render_template('mostrar_valores.html', mes_uf = mes_uf, count = mes_uf.count(),month = month,nombre_meses = meses)
    else:
        return render_template('mostrar_valores.html', mes_uf = mes_uf, count = mes_uf.count(),month = month,nombre_meses = meses) 

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)