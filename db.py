from flask_sqlalchemy import SQLAlchemy

#Generamos un objeto de SQLALQUEMY desde la extensión de flask de SQLALQUEMY para que podamos ligar la base de datos a nuestra app de manera sencilla
db=SQLAlchemy()

items={}
stores={}