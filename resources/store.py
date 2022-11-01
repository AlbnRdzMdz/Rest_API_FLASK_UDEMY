from ast import Delete
from email import message
from sqlite3 import IntegrityError
from flask import Flask,request
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db


#from db import stores

from models import StoreModel
from schemas import StoreSchema


#Un blueprint en flask smorest, se usa para dividir una API en diferentes segmentos.

blp=Blueprint("Stores",__name__,description="Operation on Stores")
#Esto irá a la documentación de Flask que veremos más adelante.

#Ahora podremos crear una clase con Method View
#Cuyos métodos nos dirijan a rutas especificas.

#La clase Store, heredará de MethodView

#El siguiente decorador, conectará flask smorest con flask method view
#Cuando hagamos la petición geo o delete a la clase Store,nos devolverá los siguientes métodos

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    
    #Requerimos del acces token para acceder a esta aplicación
    @jwt_required()
    @blp.response(200,StoreSchema)
    #Recordemos que estamos serializando los datos usando el esquema de la tienda
    #Convertirá en JSON como se indicó en el esquema de la tienda
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    @jwt_required() #Requerimos del acces token en el header para acceder a esta ubicación
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store Deleted"}
        





#ahora vamos a construir la clase tienda pero para donde únicamente realizamos consultas generales
@blp.route("/store")
class StoreList(MethodView):
    #Aquí tambipen decoramos con el esquema de marshmellow
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):
        #Verificamos que la tienda no exista ya
        store=StoreModel(**store_data)
        try:
            db.session.add(store) #Agregamos el item a la base de datos
            #Se pondrá en un lugar donde aún no está escrito en la base de de datos
            #De igual fomrma, si algo falla en el add, inmediatamente se salta al error, por lo que no se llega  ahacer le commit a la base de datos
            
            #Si hay errores se puede regresar haciendo el rollback
            
            db.session.commit() #una vez que haces el commit, se manda a la base de datos.
        #Manejamos cualquier error que la base de datos nos pueda mandar
        
        #previamente en el modelo dijimos que el nombre de la tienda tene que ser único, por lo que si tenemos algún tipo de inconsistencias en esa parte este error surgirá
        except IntegrityError:
            abort(
                400,
                message= "A store with that name already exists"
            )
        except SQLAlchemyError:
            abort(500,message="An error ocurred whil inserting the store")
        
        return store

