from db import db
#Estamos importanto el objeto de SQLAlchemy que generamos en db

class ItemModel(db.Model):
    #Mapeo entrte una fila en una tabla y una clase de Pytho por lo tanto un bojeto d Python
    __tablename__="items"# Nombramos la tabla como items
    
    #A continuación definiremos las columnas de nuestra tabla
    id= db.Column(db.Integer,primary_key=True) #Entero que será la llave primaria de la tabla
    #Por default cuando usemos POSTGRES, esto hará un autoincremento cada vez que creemos un nuevo ID
    name= db.Column(db.String(80),unique=False,nullable=False)
    #Establecemos unique como false, para que diferentes tiendas puedan tener items con el mismo nombre.
    #De igual forma que tendremos una cadena de nos más de 80 caracteres como nombre
    
    #Añadiremos una columna extra para la descripción
    description=db.Column(db.String)
    
    price =db.Column(db.Float(precision=2),unique=False,nullable=False)
    
    #La siguiente columna va a ser el link entre la tabla de items y la de tiendas
    store_id=db.Column(db.Integer,db.ForeignKey("stores.id"),unique=False,nullable=False)
    #Indicamos que será la llave foranea que conecta la tabla con la tabla :Stores Columna: id
    
    #Los valores de esta última columna tendran que concidir con los valores de id de nuestras tiendas.
    
    store = db.relationship("StoreModel",back_populates="items")
    #Traete este modelo de tiendas, que llamaremos store model
    
    #De esta forma SQLAlchemy, sabrá que la tabla de stores, será utilizada para mapear en la case store model
    
    #A continuación creamos la relación muchos a muchos haciendo uso de la tabla secundaria que relacones items con tags
    
    #Ahora sabremos que tags se encuentran relacionados con que items a través de la tabla secundaria
    tags=db.relationship("TagModel",back_populates="items",secondary="items_tags")

    
    
    
    
    
    


    
    
    
