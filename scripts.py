import pymongo
#from bson.objectid import ObjectId

# CONEXION A MONGODB ATLAS
client = pymongo.MongoClient("mongodb+srv://ggrapunsky:Tiburonloco12@cluster0.hzt0u.mongodb.net/bdreip?retryWrites=true&w=majority")
db = client["bdreip"]
collection = db["PO2022"]

#Listo todos los campos de la DB
for user in collection.find({}):
 #Actualizo y si no está creo el valor nuevo con su key
  collection.update_one(user, { "$set": { "Integrador":"nan"}})
  print("DB UPDATED")