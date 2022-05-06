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

#CREO LISTA PARA ENVIAR AL FRONT HTML
datolista = []


#API QUE ALIMENTA AL GRAFICO
@app.route('/my-first-api', methods = ['GET'])
def create_graph():
  altas = []
  ampliacion = []
  reemplazo = []
  cliente = []
  pendientes =0
  valores_alta = []
  valores_ampliacion = []
  valores_reemplazo = []
  valores_cliente = []
  valores_pendientes = [0,0,0,0,0,0,0,0,0,0,0,0]

  ##Busco data para API desde la DB - ARMAR FUNCION
  for user in collection.find({"Tipo [ALTA/AMPL]":"Alta"}):
    if(user["Fecha programada"] == ""):
      pass
    else:
      altas.append(int(user["Fecha programada"][5:7]))

  for user in collection.find({"Tipo [ALTA/AMPL]":"Ampliacion"}):
    if(user["Fecha programada"] == ""):
      pass
    else:
      ampliacion.append(int(user["Fecha programada"][5:7]))    
    
  for user in collection.find({"Tipo [ALTA/AMPL]":"Reemplazo"}):
    if(user["Fecha programada"] == ""):
      pass
    else:
      reemplazo.append(int(user["Fecha programada"][5:7]))  

  for user in collection.find({"Tipo [ALTA/AMPL]":"Cliente"}):
    if(user["Fecha programada"] == ""):
      pass
    else:
      cliente.append(int(user["Fecha programada"][5:7]))

  for user in collection.find({"$or": [
                              {"Fecha programada": {'$eq': float('NaN')}},
                              {"Fecha programada": {'$eq': ""}},
                              {"Fecha programada": {'$eq': "nan"}}  
                              ]}):
    pendientes = pendientes + 1
  valores_pendientes.append(pendientes)

  #Ordeno data para enviar a la API - ARMAR FUNCION
  for i in range(1,13):
    valores_alta.append(altas.count(i))
    valores_ampliacion.append(ampliacion.count(i))
    valores_reemplazo.append(reemplazo.count(i))
    valores_cliente.append(cliente.count(i))
  
  return jsonify({
                 "valores_alta" : valores_alta,
                 "valores_ampliacion" : valores_ampliacion,
                 "valores_reemplazo" : valores_reemplazo,
                 "valores_cliente" : valores_cliente,
                 "valores_pendientes" : valores_pendientes})




#ROUTES
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
    #Busco el objeto que recibí en la BD y lo envío al HTML para editar
    user = collection.find_one({'_id':ObjectId(id)})
    print(user)
    return render_template('editar.html', datos=list(user.values()), heads=list(user.keys()))

                           
@app.route("/update/<id>", methods = ['GET', 'POST'])
def actualiza_pedido(id):
  #print(request.form['fechaprogramada'])
  #print(type(request.form['fechaprogramada']))
  
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


