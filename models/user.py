
#Añadiremos unique ID
#username
#password


from db import db 

class UserModel(db.Model):
    __tablename__="users"
    
    #Creamos las columnas de nuestra tabla de usuarios para autenticación
    id=db.Column(db.Integer,primary_key=True)
    #ID como llave primaria
    #No puede haber más de un username, y no puede faltar en el login
    username=db.Column(db.String(80),unique=True,nullable=False)
    #No puede faltar la contraseña
    password=db.Column(db.String(80),nullable=False)
    #La contraseña no puede ser única, porque eso sería raro
    