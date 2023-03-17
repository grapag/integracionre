import pymongo
#from bson.objectid import ObjectId

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