import pymongo
#from bson.objectid import ObjectId
'''
# CONEXION A MONGODB ATLAS
client = pymongo.MongoClient("mongodb+srv://ggrapunsky:Tiburonloco12@cluster0.hzt0u.mongodb.net/bdreip?retryWrites=true&w=majority")
db = client["bdreip"]
collection = db["PO2022"]

#Listo todos los campos de la DB
#for user in collection.find({}):
 #Actualizo y si no está creo el valor nuevo con su key
 # collection.update_one(user, { "$set": { "Integrador":"nan"}})
ultimo = collection.find().sort("_id", -1).limit(1)
lista = list(ultimo)
print(lista[0]["ID"])
print("DB UPDATED")

# Modificar columnas en mongodb (collection)
newvalue = {"$rename": {"Tipo_renombrar1":"Tipo [ALTA/AMPL]"}}
collection.update_many({}, newvalue)
collection.update_many({}, {"$rename": {"Estado General_renombrar2":"Estado General"}})
collection.update_many({}, {"$rename": {"Comentario_renombrar3":"Comentario"}})
collection.update_many({}, {"$rename": {"Fecha programada_renombrar4":"Fecha programada"}})
collection.update_many({}, {"$rename": {"MesProgramado (Calculada)_renombrar5":"MesProgramado (Calculada)"}})
collection.update_many({}, {"$rename": {"Fecha liberación_renombrar6":"Fecha liberación"}})
collection.update_many({}, {"$rename": {"Mes liberado (Calculado)_renombrar7":"Mes liberado (Calculado)"}})
collection.update_many({}, {"$rename": {"Integrador_renombrar8":"Integrador"}})
collection.update_many({}, {"$rename": {"Escenario_renombrar9":"Escenario"}})


'''
# CONEXION A MONGODB ATLAS
client = pymongo.MongoClient(
    "mongodb+srv://ggrapunsky:Tiburonloco12@cluster0.hzt0u.mongodb.net/bdreip?retryWrites=true&w=majority"
)
db = client["bdreip"]
collection = db["PO2023"]

#Filtros
filter = {'Escenario': {'$all': ['Base']}}

#Filtro con valores NULL se escribe como None
filter2 = {'Escenario': None}

#Filtro de modificacion masiva para pasaje de escenarios
filter3 = {
    "$or": [{
        "ID": "213"
    }, {
        "ID": "170"
    }, {
        "ID": "247"
    }, {
        "ID": "244"
    }, {
        "ID": "233"
    }, {
        "ID": "164"
    }, {
        "ID": "171"
    }, {
        "ID": "195"
    }, {
        "ID": "200"
    }, {
        "ID": "199"
    }, {
        "ID": "243"
    }, {
        "ID": "142"
    }, {
        "ID": "106"
    }, {
        "ID": "92"
    }, {
        "ID": "140"
    }, {
        "ID": "84"
    }, {
        "ID": "53"
    }, {
        "ID": "46"
    }, {
        "ID": "91"
    }, {
        "ID": "69"
    }, {
        "ID": "22"
    }, {
        "ID": "41"
    }, {
        "ID": "143"
    }, {
        "ID": "68"
    }, {
        "ID": "34"
    }, {
        "ID": "6"
    }, {
        "ID": "83"
    }, {
        "ID": "38"
    }, {
        "ID": "8"
    }, {
        "ID": "56"
    }, {
        "ID": "169"
    }, {
        "ID": "24"
    }, {
        "ID": "12"
    }, {
        "ID": "95"
    }, {
        "ID": "3"
    }, {
        "ID": "141"
    }, {
        "ID": "31"
    }, {
        "ID": "105"
    }, {
        "ID": "50"
    }, {
        "ID": "136"
    }, {
        "ID": "35"
    }, {
        "ID": "101"
    }, {
        "ID": "147"
    }, {
        "ID": "39"
    }, {
        "ID": "73"
    }, {
        "ID": "70"
    }, {
        "ID": "163"
    }, {
        "ID": "71"
    }, {
        "ID": "80"
    }, {
        "ID": "79"
    }, {
        "ID": "162"
    }, {
        "ID": "82"
    }, {
        "ID": "93"
    }, {
        "ID": "94"
    }, {
        "ID": "123"
    }, {
        "ID": "26"
    }, {
        "ID": "13"
    }, {
        "ID": "118"
    }, {
        "ID": "116"
    }, {
        "ID": "262"
    }, {
        "ID": "263"
    }]
}

#Resultados
result = collection.find(filter=filter)
result2 = collection.find(filter=filter2)
result3 = collection.find(filter=filter3)

"""
contador = 0
for dato in result3:
    #print(dato)
    contador += 1

print("Escenarios Base:", contador)

"""
contador = 0
for dato in result3:
    print(dato)
    collection.update_one(dato, {"$set": {"Escenario": "Baja"}})
    contador += 1

print("Escenarios Vacíos:", contador)
