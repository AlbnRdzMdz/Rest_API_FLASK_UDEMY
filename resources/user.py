from venv import create
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
#Passlib nos ayuda a hashear la contraseña del usuario con un algoritmo especifico
#Digamos que el usuario se registra con 12345 como pass
#convertiremos esto en kajdnkjNDLSVKJNZK.VJNDZKXJC,VNLX,JMC,XJCMN LD.ZK,JXMNV
#Y ESO ALMACENAREMOS EN LA BASE DE DATOS
#Compararemos en la base de datos cuando volvamosa recibir la contraseña si el hash es el almacenado
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt,get_jwt_identity
#es una combinación de numeros y caracteres que vamos a generar en el servidor, mandarlo al cliente y que tenga acceso a ciertas direcciones.
#La única forma de que el usuario tenga acceso a un token que gereraremos en el servidor es mediante el usuario y contraseña correctos

from flask_jwt_extended import jwt_required

#Importamos la lista

from blocklist import BLOCKLIST



from db import db
from models import UserModel
from schemas import UserSchema


blp = Blueprint("Users", "users", description="Operations on users")

#Generamos el endpoint para el registro de usuario

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201
    

#Vamos a generar el recurso para el login

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
    #Verificamos la existencia del usuario (una vez que sabemos que existe)
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            #Verificamos que la contraseña que nos mandó el usuario, pueda ser hasheada tal como la versión que fue almacenada en la base de datos
            #No lo deshasheamos
            #Podemos checar que el usuario y el pass sean válidos
            acces_token = create_access_token(identity=user.id,fresh=True) #importante mencionar que Fresh=True ya que estaremos trabajando tambien con tokens (no frejcos)
            #vamos también a crear un refresh token
            refresh_token=create_refresh_token(identity=user.id)
            return {"acces_token":acces_token,"refresh_token":refresh_token}
        
        
        abort(401,message="Invalid Credentials")
        

#Creamos el endpoint para el refreshtoken

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity() #returns none if there´s no current user
        new_token=create_access_token(identity=current_user,fresh=False)
        #Es importante el false, de lo contrario, podríamos estar generando tokens frecos con los token no-frescos, y no queremos eso
        #Queremos que todos los tokens que genere el token no freco para actualizarse, sean no frescos, y así se tendrá un trato diferente según el endpoint en el que se trabaja con respecto a si se tienen acciones constructivas o destructivas
        
        #Queremos poder generar únicamente el refreshtoken 1 vez, y que este ya no pueda generar más non-freshtokens
        jti=get_jwt()["jti"]
        BLOCKLIST.add(jti)    
        
        return{"acces_token":new_token}






#LOGOUT de usuario

@blp.route("/logout")
class UserLogout(MethodView):
    #Solicitamos el jwt
    @jwt_required()
    def post(self):
        #Tomar el JWT unique identifier
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        #Añadirlo al conjunto de tokens bloqueados
        return {"message": "Successfully logged out"}, 200



#en una ruta nueva

@blp.route("/user/<int:user_id>")
#Cabe recalcar el hecho de que el ID debe ser una cadena porque así lo especiicamos en la base de datos.

class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    #Usando el esquema de usuario, podremos regresar el ID de usuario en caso de existir,
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    #De igual forma podemos borrar un usuario
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        
        return {"Message":"User deleted succesfully"}
    
    
        
        