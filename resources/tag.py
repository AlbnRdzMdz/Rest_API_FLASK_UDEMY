import uuid
from flask import Flask,request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
#Importamos el error de SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import jwt_required

#Importamos los modelos de tienda y tag que trabajaran juntos
from db import db

from models import TagModel,StoreModel,ItemModel
from models.item import ItemModel
 
from schemas import TagSchema,TagAndItemSchema #Importamos el esquema de Tags


blp = Blueprint("Tags","tags",description="Operations on tags")


#Ahora vamos a crear algunos endpoint nuevos.

#Rutas para la creación y retorno de tags en una tienda

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    
    @jwt_required()
    @blp.response(200,TagSchema(many=True))
    #Get nos dará una lista de los tags que se encuentran dispoibles en la tienda
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    #para crear un tag en una tienda, necesitamos el objeto de tag (crearlo)
    def post(self,tag_data,store_id):
        tag=TagModel(**tag_data,store_id=store_id)
        
        #Si queremos checar el nombre podemos filtrar por el stroe_id
        #NOs dirá que otros tags tienen el mismo store ID
        
        #El nombre del tag y el store ID
        
        
        try:
            db.session.add(tag)
            db.session.commit()
        #Pasamos el error como un mensaje.
        except SQLAlchemyError as e:
            abort(
                500,message=str(e)
            )
        return tag
        
        
        #Veamos si podemos regresar infromación de un TAG en especifico dado en ID

#Añadimos endpoint para añadir tad a item
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    #Respondemos con el esquema de tag
    @blp.response(201,TagSchema)
    def post(self,item_id,tag_id):
        #Lo primero que queremos es verificar que existan el tag y el item
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        #Si cualquiera de ellos no exite tendremos un 404
        
        #Trataremos los tags como una lista gracias a SQLAlchemy
        item.tags.append(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error ocurred while inserting the tag. ")
        
        return tag
    
    @jwt_required()
    @blp.response(201,TagAndItemSchema)
    def delete(self,item_id,tag_id):
        #Lo primero que queremos es verificar que existan el tag y el item
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        #Si cualquiera de ellos no exite tendremos un 404
        
        #Trataremos los tags como una lista gracias a SQLAlchemy
        item.tags.remove(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error ocurred while removing the tag. ")
        
        return {"message": "Item removed from tag","item":item,"tag":tag}
    
    


 
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self,tag_id):
        tag= TagModel.query.get_or_404(tag_id)
        return tag
    
    #Podemos usar este endpoint para borrar también.
    #Podríamos tener diferentes respuestas:
    
    @blp.response(
        200,
        description="Deletes a tag if no item is tagged with it",
        example={"message":"tag"}
    )
    @blp.alt_response(404,description="Tag not found.")
    
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted")
    
    def delete(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag deleted"}
        
          
        
            
        