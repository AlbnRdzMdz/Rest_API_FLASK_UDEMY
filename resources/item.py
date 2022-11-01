from flask import Flask,request

from flask.views import MethodView
from flask_smorest import Blueprint, abort
#Importamos el error de SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

#Podemos importar un módulo que nos permita solicitar el jwt para acceder al endopoint
from flask_jwt_extended import jwt_required,get_jwt

#from db import items

#Ojo que remplazamos el diccionario que fungía de base de datos
from db import db

from models import ItemModel
 
from schemas import ItemSchema, ItemUpdateSchema


#Un blueprint en flask smorest, se usa para dividir una API en diferentes segmentos.

blp=Blueprint("Items",__name__,description="Operation on Items")
#Esto irá a la documentación de Flask que veremos más adelante.

#Ahora podremos crear una clase con Method View
#Cuyos métodos nos dirijan a rutas especificas.

#La clase Item, heredará de MethodView

#El siguiente decorador, conectará flask smorest con flask method view
#Cuando hagamos la petición get o delete a la clase Item,nos devolverá los siguientes métodos

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    #main response
    @blp.response(200, ItemSchema)
    def get(self,item_id):
        #Vamos a utilizar la información en la URL de la tienda de la que el cliente quiere visualizr la información.
        item = ItemModel.query.get(item_id)
        #Regresa el item desde la base de datos, utilizando la llave primaria del item 
        #para eso es el get:
        #Si no hay esta llave, automáticamente regresará un error 404
        
        return item
    
        #El atributo query de la clase del modelo se hereda desde db.Model, que a asu ves se hereda de FLASK SQLAlchemy
        
    @jwt_required()
            
    def delete(self,item_id):
        #Verificamos que se tengan privilegios de admin
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
            #En caso de no tener privilegios de admin (usuario ID diferente de 1 en este caso)
        
        
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item Deleted"}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)#Verifica los argumentos de entrada con el esquema de Marshmellow
    @blp.response(200,ItemSchema) #Verifica los datos de salida con el mismo esque para el PUT
    #######
    ###EL orden de los decoradores importa, primero van los argumentos y después la respuesta.
    def put(self,item_data,item_id):
        item = ItemModel.query.get(item_id)
        #Debemos considerar que si el item existe, solo lo actualizaremos, de lo contrario lo crearemos con el modelo que ya establecimos previamente
        
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]# De estas formas estamos actualizando el item
        else:
            #Lo creamos con el modelo de item que definimos previamente.
            item= ItemModel(id=item_id,**item_data)
            #Si no existe, necesitaremos nombre, precio y stroe ID  según lo establecido en el esque,a
            
        #Subimos a la base de datos y hacemos el commit
        db.session.add(item)
        db.session.commit()
        
        
        db.session
        
        return item




#ahora vamos a construir la clase tienda pero para donde únicamente realizamos consultas generales
@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    #Estaremos regresando una lista de items
    
    #Verificamos que el usuario se haya logeado para acceder a este endpoint
    @jwt_required(fresh=True)
    #necesitaremos un token fresco (generado con usuario y contraseña) para poder realizar el post de un ITEM
    #esto podrémos hacerlo en todos los endpoints que nos interese protejer de manera activa
    
    #A continuación vamos a introducir el esquema de marshmellow para la validadción de los datos
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        item=ItemModel(**item_data)
        try:
            db.session.add(item) #Agregamos el item a la base de datos
            #Se pondrá en un lugar donde aún no está escrito en la base de de datos
            #De igual fomrma, si algo falla en el add, inmediatamente se salta al error, por lo que no se llega  ahacer le commit a la base de datos
            
            #Si hay errores se puede regresar haciendo el rollback
            
            db.session.commit() #una vez que haces el commit, se manda a la base de datos.
        #Manejamos cualquier error que la base de datos nos pueda mandar
        except SQLAlchemyError:
            abort(500,message="An error ocurred whil inserting the item")

        
        
        return item
    