import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from replit import db, web
from flask_pymongo import PyMongo

# -- Create & configure Flask application.
app = flask.Flask(__name__)
app.config['MONGO_URI']='mongodb://ggrapunsky:Tiburonloco12@cluster0.qagbp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
#app.static_url_path = "/static"

mongo = PyMongo(app)

users = web.UserStore()

@app.route("/", methods=['GET', 'POST'])
def Index():
    return flask.render_template("index.html")

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
      print("Datos guardados correctamente")
      return redirect('Index')
      #return flask.render_template("index.html")
#web.run(app)
      
# starting the app
if __name__ == "__main__":
    #app.run(debug=true)
    web.run(app)