from audioop import lin2adpcm
from flask import Flask,request
import os
from flask_smorest import Api
#Improtamos la librería de autenticación de ususarios
from flask_jwt_extended import JWTManager

#Vamos a importar el módulo para hacer las miagraciones de la base de datos
#Esto nos permite hacer modificaciones a nuestros modelos y tablas en la base de datos sin arriesgar la infromación

from dotenv import load_dotenv

#Modificaciones

from flask_migrate import Migrate


from flask import jsonify
#Importamos la lista de tokens que ya no son válidos
from blocklist import BLOCKLIST

import secrets
#Secrets, nos ayudará a generar la clave de nuestra llave secreta

from db import db
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBluePrint

 
def create_app(db_url=None):
    app= Flask(__name__)
    #Esto crea una app de flask
    #una vez que se definan los endpoints, dichos puntos estarán acesibles al cliente una vez que el servidor se corra

    #Creamos una llave secreta para que cuando el usuario nos envíe un archivo de jwt, se pueda verificar que la clave del usuario haya sido creada
    #app.config["JWT_SECRET_KEY"]="jose"
    #Es importante que esta llave secreta sea compleja, porque si el ususario la descubre podría autenticarse sin que nosotros tengamos el control de eso
    #app.config["JWT_SECRET_KEY"]=secrets.SystemRandom().getrandbits(128)#128 bits de ongitud
    #Ahora,no queremos cambiar la llave cada vez que reiniciemos la app
    #por lo que ejecutamos dicho método en terminal y usamos el número generado como llave
    
    load_dotenv()
    app.config["JWT_SECRET_KEY"]="1200654314856573955517327440138917444"#128 bits de ongitud

    
    #Es importante porque las JWT, almacenan cierta infromación

    #Crearemos una instancia del administrador de JWT
    jwt=JWTManager(app)
    
    
    #Verificamos que el token no exista ya en la lita de tokens que hicieron logout
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    #Cuando regresemos un JWT, se ejecuta, si esta función regresa verdadero
    #La función se termina y el usuario recibe un error ya que el usuario hizo ya logout
    
    #Pero para mandar un mensaje y comunicar al usuario este error simplemente hacemos logout
    #llamamos otro decorador que tambipen decora una función que consume el ancabezado y la carga del json
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
    
    
    #Verificamos informaicón extra sobre los usuarios registrados 
    #Si son o no administradores por ejemplo:
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    
    
    #Aquí añadiremos algunos manejos de errores:
    #Si el token ha expirado.
    @jwt.expired_token_loader
    #Esta función toma como argumento el jwtheader y la carga y verifica que no hayan expirado
    def expired_token_callback(jwt_header,jwt_payload):
        return (
            jsonify({"message":"THe token has expired","error":"token_expired"}
        ),401,
        )
    #Regresamos una tupla con el jason y el codigo de status
    
    #Vamos a verificar que el token sea válido
    #Aquellas funciones que toma como argumento un error son las que o no cuentan con el jwt o el dado no es válido
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    #Verificamos que el header contenga el token
    #De lo contrario regresaremos el error mostrado 
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )    
    

    #Configuraciones:

    app.config["PROPAGATE_EXCEPTIONS"]= True

    #Y algunas configuracioones respecto a la documentación que vamos a generar de nuestra API
    #Titulo y version
    app.config["API_TITLE"]="Stores REST API"
    app.config["API_VERSION"]="v1"
    #El standar a utilizar para la documentación de la API
    app.config["OPENAPI_VERSION"]="3.0.3"
    #Le dice a flask smorest donde está nuestra API
    #A continuación le decimos donde empiezan nuestros endpoints con respecto  al carpeta en la que nos encontramos.
    app.config["OPENAPI_URL_PREFIX"]="/"
    #Por último le dice a Flask smorest que use swagger para realizar la documentación y de donde se descargará el código que ayude  ahace rla docuemtnación
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL","sqlite:///data.db") #Aquí se almacenará nuestra infromación
    #Vamosa modificar un parámetro de SQLAlchemy que lo alentiza y ya no es necesario
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    
    #Inicializamos nuestra base de datos en nuestra app
    db.init_app(app)
    
    #Agregamos la funcionalidad con flask migrate a la app apra ser capaces de relizar las migraciones
    
    migrate=Migrate(app,db)# importante crearlo después de db.init_app
    
    
    #Como ya estamos utilizando Flask-migrate para crear las tablas de nuestra base de datos, no necesitaremos más SQLALchemy
    #por lo que comentaremos las siguientes lineas de código
    
    """
    with app.app_context():
        db.create_all()"""
        
    #A estas alturas SQLAlchemy ya sabe que tablas vamos a crear porque importamos previamente los modelos
    
    #Hecho esto vamos a conetar la extensión de flask smorest con la app principal de flask

    api= Api(app)
    #Que son las clases que definimos en nuestro folder de recursos

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBluePrint)
    

    
    return app


