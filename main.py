import flask
from flask import Flask, render_template, redirect, url_for, flash
from flask import jsonify, request, send_file, make_response
from io import StringIO
import csv
from replit import db, web
import pymongo
from bson.objectid import ObjectId

# Crear & configurar Flask app.
app = Flask(__name__)
users = web.UserStore()

# CONEXION A MONGODB ATLAS
client = pymongo.MongoClient(
    "mongodb+srv://ggrapunsky:Tiburonloco12@cluster0.hzt0u.mongodb.net/bdreip?retryWrites=true&w=majority"
)
db = client["bdreip"]
#coleccion BD 2022
collection = db["PO2023"]
#coleccion BD 2023
collection_22 = db["PO2022"]


#CREO LISTA PARA ENVIAR AL FRONT HTML
datolista = []


#API QUE ALIMENTA AL GRAFICO
@app.route('/api', methods=['GET'])
def create_graph():
    altas = []
    ampliacion = []
    reemplazo = []
    cliente = []
    ampliacion_placas = []
    pendientes = 0
    valores_alta = []
    valores_ampliacion = []
    valores_reemplazo = []
    valores_cliente = []
    valores_ampliacion_placas = []
    valores_pendientes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    estadoGral_NI = 0
    estadoGral_EC = 0
    estadoGral_EL = 0
    estadoGral_LI = 0
    estadoGral_PE = 0
    alorenzo_prodxmes = []
    ebarbero_prodxmes = []
    jvilar_prodxmes = []
    jschmukler_prodxmes = []

    ##Busco data del grafico Bar para API desde la DB - ARMAR FUNCION
    for user in collection.find({"Tipo [ALTA/AMPL]": "Alta"}):
        if (user["Fecha programada"] == ""):
            pass
        else:
            altas.append(int(user["Fecha programada"][5:7]))

    for user in collection.find({"Tipo [ALTA/AMPL]": "Ampliacion"}):
        if (user["Fecha programada"] == ""):
            pass
        else:
            ampliacion.append(int(user["Fecha programada"][5:7]))

    for user in collection.find({"Tipo [ALTA/AMPL]": "Reemplazo"}):
        if (user["Fecha programada"] == ""):
            pass
        else:
            reemplazo.append(int(user["Fecha programada"][5:7]))

    for user in collection.find({"Tipo [ALTA/AMPL]": "Cliente"}):
        if (user["Fecha programada"] == ""):
            pass
        else:
            cliente.append(int(user["Fecha programada"][5:7]))

    for user in collection.find({"Tipo [ALTA/AMPL]": "Ampliacion_Placas"}):
        if (user["Fecha programada"] == ""):
            pass
        else:
            ampliacion_placas.append(int(user["Fecha programada"][5:7]))

    for user in collection.find({
            "$or": [{
                "Fecha programada": {
                    '$eq': float('NaN')
                }
            }, {
                "Fecha programada": {
                    '$eq': ""
                }
            }, {
                "Fecha programada": {
                    '$eq': "nan"
                }
            }]
    }):
        pendientes = pendientes + 1
    valores_pendientes.append(pendientes)

    ##Busco data del grafico Torta para API desde la DB - ARMAR FUNCION
    for user in collection.find({"Estado General": {"$exists": True}}):
        if (user["Estado General"] == "No Iniciado"):
            estadoGral_NI += 1
        elif (user["Estado General"] == "En Construccion"):
            estadoGral_EC += 1
        elif (user["Estado General"] == "En Liberacion"):
            estadoGral_EL += 1
        elif (user["Estado General"] == "Liberado"):
            estadoGral_LI += 1
        else:  #Caso donde el estado Gral es Vacio o Null => Pendiente
            estadoGral_PE += 1

    ##Busco data para armar el grafico de produccion x integrador - ARMAR FUNCION
    for i in range(1, 13):
        alorenzo_prod = 0
        ebarbero_prod = 0
        jvilar_prod = 0
        jschmukler_prod = 0
        for user in collection.find({
                "Estado General": "Liberado",
                "Mes liberado (Calculado)": i
        }):
            if (user["Integrador"] == "Andres Lorenzo"):
                alorenzo_prod += 1
            elif (user["Integrador"] == "Enzo Barbero"):
                ebarbero_prod += 1
            elif (user["Integrador"] == "Javier Vilar"):
                jvilar_prod += 1
            elif (user["Integrador"] == "Jorge Schmukler"):
                jschmukler_prod += 1
            else:
                pass
        alorenzo_prodxmes.append(alorenzo_prod)
        ebarbero_prodxmes.append(ebarbero_prod)
        jvilar_prodxmes.append(jvilar_prod)
        jschmukler_prodxmes.append(jschmukler_prod)

    #Ordeno data del bar char para enviar a la API - ARMAR FUNCION
    valor_alorenzo_prod = 0
    valor_ebarbero_prod = 0
    valor_jvilar_prod = 0
    valor_jschmukler_prod = 0

    for i in range(1, 13):
        valores_alta.append(altas.count(i))
        valores_ampliacion.append(ampliacion.count(i))
        valores_reemplazo.append(reemplazo.count(i))
        valores_cliente.append(cliente.count(i))
        valores_ampliacion_placas.append(ampliacion_placas.count(i))
        valor_alorenzo_prod += alorenzo_prodxmes[i - 1]
        valor_ebarbero_prod += ebarbero_prodxmes[i - 1]
        valor_jvilar_prod += jvilar_prodxmes[i - 1]
        valor_jschmukler_prod += jschmukler_prodxmes[i - 1]

    #Devuelvo API JSON
    return jsonify({
        "valores_alta": valores_alta,
        "valores_ampliacion": valores_ampliacion,
        "valores_reemplazo": valores_reemplazo,
        "valores_cliente": valores_cliente,
        "valores_ampliacion_placas": valores_ampliacion_placas,
        "valores_pendientes": valores_pendientes,
        "estadoGral_NI": estadoGral_NI,
        "estadoGral_EC": estadoGral_EC,
        "estadoGral_EL": estadoGral_EL,
        "estadoGral_LI": estadoGral_LI,
        "estadoGral_PE": estadoGral_PE,
        "alorenzo_prodxmes": alorenzo_prodxmes,
        "valor_alorenzo_prod": valor_alorenzo_prod,
        "ebarbero_prodxmes": ebarbero_prodxmes,
        "valor_ebarbero_prod": valor_ebarbero_prod,
        "jvilar_prodxmes": jvilar_prodxmes,
        "valor_jvilar_prod": valor_jvilar_prod,
        "jschmukler_prodxmes": jschmukler_prodxmes,
        "valor_jschmukler_prod": valor_jschmukler_prod,
    })


#ROUTES
@app.route("/", methods=['GET', 'POST'])
def Index():
    #Limpio la lista, para cargarla luego de las actualizaciones
    datolista.clear()
    po=request.args.get('po')
  
    if po=="2022": #capturo datos por URL perteneciente al PO y defino que BD utilizar
      for document in collection_22.find({}):
          #Armo lista de documentos que vienen de la BD para enviar al Front
          datolista.append(document)
      #Lista de las cabeceras del diccionario
      listaheads = list(datolista[0].keys())
      return flask.render_template("index.html",
                                   datos=datolista,
                                   heads=listaheads)
      
    else: #Al no recibir datos por URL perteneciente al PO utilizo la BD del PO actual
      for document in collection.find({}):
        #Armo lista de documentos que vienen de la BD para enviar al Front
        datolista.append(document)
      #Lista de las cabeceras del diccionario
      listaheads = list(datolista[0].keys())
      return flask.render_template("index.html",
                                     datos=datolista,
                                     heads=listaheads)

@app.route("/imadmin", methods=['GET', 'POST'])
def Index_admin():
    #Limpio la lista, para cargarla luego de las actualizaciones
    datolista.clear()
    po=request.args.get('po')
  
    if po=="2022": #capturo datos por URL perteneciente al PO y defino que BD utilizar
      for document in collection_22.find({}):
          #Armo lista de documentos que vienen de la BD para enviar al Front
          datolista.append(document)
      #Lista de las cabeceras del diccionario
      listaheads = list(datolista[0].keys())
      return flask.render_template("index_admin.html",
                                   datos=datolista,
                                   heads=listaheads,
                                   po=po)
      
    else: #capturo datos por URL perteneciente al PO y defino que BD utilizar
      for document in collection.find({}):
          #Armo lista de documentos que vienen de la BD para enviar al Front
          datolista.append(document)
      #Lista de las cabeceras del diccionario
      listaheads = list(datolista[0].keys())
      return flask.render_template("index_admin.html",
                                   datos=datolista,
                                   heads=listaheads,
                                   po="")

@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_data(id):
    if request.method == 'POST':
      po=request.args.get('po')

      if po=="2022": #capturo datos por URL perteneciente al PO y defino que BD utilizar
        #Busco el objeto que recibí en la BD y lo envío al HTML para editar
        user = collection_22.find_one({'_id': ObjectId(id)})
        print(user)
        return render_template('editar.html',
                               datos=list(user.values()),
                               heads=list(user.keys()),
                               po=po)
        
      else: #capturo datos por URL perteneciente al PO y defino que BD utilizar
        #Busco el objeto que recibí en la BD y lo envío al HTML para editar
        user = collection.find_one({'_id': ObjectId(id)})
        print(user)
        return render_template('editar.html',
                               datos=list(user.values()),
                               heads=list(user.keys()),
                               po=po)


@app.route('/update/<id>', methods=['GET', 'POST'])
def actualiza_pedido(id):
    #print(request.form['fechaprogramada'])
    #print(type(request.form['fechaprogramada']))
    
    if (request.form['fechaprogramada'] == ""):
        fechaprog = "nan"
    else:
        fechaprog = int(request.form['fechaprogramada'][5:7])

    if (request.form['fechaliberacion'] == ""):
        fechalib = "nan"
    else:
        fechalib = int(request.form['fechaliberacion'][5:7])

    if request.method == 'POST':
        po=request.args.get('po')
        #estadopedido = request.form['estadopedido']
        newvalues = {
            "$set": {
                "Nuevo Key": request.form['nuevokey'],
                "Tipo [ALTA/AMPL]": request.form['tipopo'],
                "Estado General": request.form['estadogral'],
                "Comentario": request.form['comments'],
                "Fecha programada": request.form['fechaprogramada'],
                "MesProgramado (Calculada)": fechaprog,
                "Fecha liberación": request.form['fechaliberacion'],
                "Mes liberado (Calculado)": fechalib,
                "Integrador": request.form['integrador']
            }
        }
    
    if po=="2022": #capturo datos por URL perteneciente al PO y defino que BD utilizar
      #Busco el objeto seleccionado de mi front en la DB
      user = collection_22.find_one({'_id': ObjectId(id)})
      #Actualizo la DB con los nuevos valores
      collection_22.update_one(user, newvalues)
      print("DB UPDATED")

    else: #capturo datos por URL perteneciente al PO y defino que BD utilizar
      #Busco el objeto seleccionado de mi front en la DB
      user = collection.find_one({'_id': ObjectId(id)})
      #Actualizo la DB con los nuevos valores
      collection.update_one(user, newvalues)
      print("DB UPDATED")
        
    return redirect(url_for('Index_admin'))


@app.route('/add', methods=['GET', 'POST'])
def agrega_pedido():
  
    #Busca el ultimo registro para identificar el nro de ID
    ultimo = collection.find().sort("_id", -1).limit(1)
    ultimo_id = int(list(ultimo)[0]["ID"])

    #Calcula el TIPO RE
    if (request.values.get('po') == "PO2023_RELH"):
        tipore = "RELH"
    else:
        tipore = "REIP"

    #Calcula si es RE CLIENTE
    if (request.values.get('po') == "PO2023_REIP_Cliente"):
        escliente = "Si"
    else:
        escliente = "nan"

    #Calcula los CDL desde los Nodos ingresados
    cdla = request.values.get('nodoa')[0:3]
    cdlb = request.values.get('nodob')[0:3]
    acronimos = request.values.get('key').split("-")

    if request.method == 'GET':
        #Nuevos valores que se ingresarán a la BD
        newvalues = {
            "ID": ultimo_id + 1,
            "Tipo RE": tipore,
            "Key": request.values.get('key'),
            "Tipo Plan de Obra": "nan",
            "PO2022": request.values.get('po'),
            "Version": "nan",
            "Accion_Planif": request.values.get('accionplanif'),
            "Config Obj Planif": "nan",
            "Observacion PO2022": request.values.get('obspo'),
            "Es para un cliente?": escliente,
            "Q Planificado": "nan",
            "Region": request.values.get('region'),
            "Provincia_A": "nan",
            "Provincia_B": "nan",
            "Nodo A": request.values.get('nodoa'),
            "Nodo B": request.values.get('nodob'),
            "Acronimo_A": acronimos[0],
            "Marca_A": request.values.get('marcaa'),
            "Modelo_A": "nan",
            "CDL_A": cdla,
            "SLS_A": "nan",
            "Nombre_A": request.values.get('nombrea'),
            "Acronimo_B": acronimos[1],
            "Vendor_B": request.values.get('marcaa'),
            "Modelo_B": "nan",
            "CDL_B": cdlb,
            "SLS_B": "nan",
            "Nombre_B": request.values.get('nombreb'),
            "Total (USD)": "nan",
            "Nuevo Key": "nan",  ##VALORES QUE INGRESAN X WEB
            "Tipo [ALTA/AMPL]": "nan",
            "Estado General": "nan",
            "Comentario": "nan",
            "Fecha programada": "nan",
            "MesProgramado (Calculada)": "nan",
            "Fecha liberación": "nan",
            "Mes liberado (Calculado)": "nan",
            "Integrador": "nan"
        }

    #Inserto en la DB los nuevos valores
    collection.insert_one(newvalues)
    print("DB UPDATED")

    return redirect(url_for('Index_admin'))


@app.route('/download', methods=['GET', 'POST'])
def post():
    csvList = []
    index = 0
    po=request.args.get('po')
    
    if po=="2022": #capturo datos por URL perteneciente al PO y defino que BD utilizar
      #Consulto la DB para armar los datos a enviar al exportador de CSV
      for document in collection_22.find({}):
          if (index == 0):  #Si es el primero, armo los headers del archivo
              listOfKeys = document.keys()
              listOfKeys = list(listOfKeys)
              csvList.append(listOfKeys)
              index = 1
          else:
              pass

    else: #capturo datos por URL perteneciente al PO y defino que BD utilizar
      #Consulto la DB para armar los datos a enviar al exportador de CSV
      for document in collection.find({}):
          if (index == 0):  #Si es el primero, armo los headers del archivo
              listOfKeys = document.keys()
              listOfKeys = list(listOfKeys)
              csvList.append(listOfKeys)
              index = 1
          else:
              pass
            
    #Armo lista de lista de valores del archivo csv [rows]
    listOfValues = document.values()
    listOfValues = list(listOfValues)
    csvList.append(listOfValues)
    #Comienzo con la exportacion del CSV
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(csvList)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

###  DATA GRAFICOS  ###
@app.route("/datagral", methods=['POST', 'GET'])
def get_dataGral_graph():
    dataSelected = request.json
    if request.method == 'POST':
      datobd = []
      #Limpio la lista, para cargarla luego de las actualizaciones
      datobd.clear()
      contadorSelected=0
      for document in collection.find({}):
        if((dataSelected["name"] == "Liberado") or (dataSelected["name"] == "En Liberacion")):
          if(document["Estado General"] == dataSelected["name"]):
            contadorSelected=contadorSelected+1
          #Armo lista de documentos que vienen de la BD para enviar al Front
            datobd.append(document)
        else:
          if(document["Estado General"] != "Liberado" and document["Estado General"] != "En Liberacion"):
          #Armo lista de documentos que vienen de la BD para enviar al Front
            contadorSelected=contadorSelected+1
            datobd.append(document)
        #Lista de las cabeceras del diccionario
      listaheads = list(document.keys())
      print(contadorSelected)
      return flask.render_template('datagral.html',heads=listaheads,datos=datobd,contador=contadorSelected,data=dataSelected["name"])
    #return ('', 204)



### ACTIVIDADES RE ###
@app.route("/actividadre", methods=['GET', 'POST'])
def actividadre():
  print("opening function in backend linked to actividadre")
  return flask.render_template('actividadre.html')

  
###  BACKHAULING  ###
@app.route("/bhtemplates", methods=['GET', 'POST'])
def bhtemplates():
    #ARMAR FUNCIONALIDADES
    config = []
    archivo = open("Configs/Config_Huawei.txt")
    while (True):
        linea = archivo.readline()
        config.append(linea)
        #revisar si la linea no es null
        if not linea:
            break
    #cerramos el archivo
    archivo.close
    return flask.render_template("bhtemplates.html", config=config)


# Inicializando la app
if __name__ == "__main__":
    web.run(app, debug=False)
