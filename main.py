import flask
from flask import Flask, render_template, redirect, url_for, flash
from flask import jsonify, request, send_file
from replit import db, web
#import pandas as pd
import pymongo
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

# Crear & configurar Flask app.
app = Flask(__name__)

users = web.UserStore()

# CONEXION A MONGODB ATLAS
client = pymongo.MongoClient("mongodb+srv://ggrapunsky:Tiburonloco12@cluster0.hzt0u.mongodb.net/bdreip?retryWrites=true&w=majority")
db = client["bdreip"]
collection = db["PO2022"]

#Creo lista para enviar al front HTML
datolista = []

#OTRA RUTA
@app.route('/my-first-api', methods = ['GET'])
def hello():
  name = request.args.get('name')

  xaxis = ['Apples', 'Oranges', 'Bananas']
  serie1_nombre = "sogan" 
  serie1_data = [8, 4, 3]
  
  if name is None:
    text = 'Hello!'

  else:
    text = 'Hello ' + name + '!'

  return jsonify({"xaxis": xaxis,
                 "serie1_nombre" : serie1_nombre,
                 "serie1_data" : serie1_data})




#Routes
@app.route("/", methods=['GET', 'POST'])
def Index():
  #Limpio la lista, para cargarla luego de las actualizaciones
  datolista.clear()
  for document in collection.find({}):
    #Armo lista de documentos que vienen de la BD para enviar al Front
    datolista.append(document)
  #Lista de las cabeceras del diccionario
  listaheads = list(datolista[0].keys())      
  return flask.render_template("index.html", datos=datolista, heads=listaheads)


@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_data(id):
  if request.method == 'POST':
    #Busco el objeto que recibí en la BD y lo envío a la pagina para editar
    user = collection.find_one({'_id':ObjectId(id)})
    print(user)
    return render_template('editar.html', datos=list(user.values()), heads=list(user.keys()))

                           
@app.route("/update/<id>", methods = ['GET', 'POST'])
def actualiza_pedido(id):
  if(request.form['fechaprogramada'] == ""):
    fechaprog = "nan"
  else:
    fechaprog = int(request.form['fechaprogramada'][5:7])
  
  if(request.form['fechaliberacion'] == ""):
    fechalib = "nan"
  else:
    fechalib = int(request.form['fechaliberacion'][5:7])
  
  if request.method == 'POST':
    #estadopedido = request.form['estadopedido']
    newvalues = { "$set": { "Nuevo Key": request.form['nuevokey'],
                           "Tipo [ALTA/AMPL]":request.form['tipopo'],
                           "Estado General":request.form['estadogral'],
                           "Comentario":request.form['comments'],
                           "Fecha programada":request.form['fechaprogramada'],
                           "MesProgramado (Calculada)":fechaprog,
                           "Fecha liberación":request.form['fechaliberacion'],
                           "Mes liberado (Calculado)":fechalib
                          } }

    #Busco el objeto seleccionado de mi front en la DB
    user = collection.find_one({'_id':ObjectId(id)})
    #Actualizo la DB con los nuevos valores
    collection.update_one(user, newvalues)
    print("DB UPDATED")
        
    return redirect(url_for('Index'))


# Inicializando la app
if __name__ == "__main__":
  web.run(app, debug=True)


