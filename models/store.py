from db import db




#Estamos importanto el objeto de SQLAlchemy que generamos en db

class StoreModel(db.Model):
    #Mapeo entrte una fila en una tabla y una clase de Pytho por lo tanto un bojeto d Python
    __tablename__="stores"# Nombramos la tabla como items
    
    #A continuación definiremos las columnas de nuestra tabla
    id= db.Column(db.Integer,primary_key=True) #Entero que será la llave primaria de la tabla
    #Por default cuando usemos POSTGRES, esto hará un autoincremento cada vez que creemos un nuevo ID
    name= db.Column(db.String(80),unique=False,nullable= False)
    
    #Ahora asociaremos la tabla de tiendas con la tabla de items mediante otra llave foranea
    items= db.relationship("ItemModel",back_populates="store",lazy="dynamic")
    #lazy=Dynamic, significa que no vamos a estar mandando a llamar a los items a menos que así se indique, como veremos más adelante
    
    
    #Como podemos notar, no  hay un ITEM-ID en esta clase pero si tenemos la relación que acabamos de establecer para linkear ambas tablas.
    
    #Agregamos la relación de las tiendas con sus multiples tags
    #UNO A MUCHOS
    
    tags=db.relationship("TagModel",back_populates="store",lazy="dynamic")
    #Si no usamos lazy = dynamic las consultas se pueden vovler lentas
    
    
    
    