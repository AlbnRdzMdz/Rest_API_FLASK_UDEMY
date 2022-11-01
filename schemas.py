
from marshmallow import Schema, fields

#Que define un item

#vamos a generar una clase para items que herede de Schema

class PlainItemSchema(Schema):
    #Este será un esquema de ítems que no sepa absolutamente nada de las tiendas
    #Usaremos este esquema cuando queramos incluir un item en una tienda, pero no queramos añadir nada más de información sobre la tienda a ella.
    
    #Aquí definiremos los campos y como se comportarán en terminos de entrada y salida
    id = fields.Int(dump_only=True)#Cadena
    #Ahora podemos definir si va a estar trabajando al consumir datos en un request o si solo va a regresar datos
    #Lo que estamos es apartando laa variable id para únicamente regresar información a partir de la API, no para recibir
    name = fields.Str(required=True)
    #Name será un campo siempre requerido entre los datos de entrada.
    price =fields.Float(required=True)
    ####
    #Solamente name, price y store_id, serán usados para validación entre los datos de entrada.
    
#De igual froma añadiremos un esquema plano para tienda
#Por último cuando trabajamos en con una tienda

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True) # Vamos a regresar el ID de la tienda.
    name = fields.Str() # Requerimos del nombre de la tienda.    

#Tenemos otros requerimentos para los datos, según lo que pretendemos hacer en nuestra aplicación
#por ejemplo cuando queremos actualizar los datos

#En este caso solo requerimos nombre y precio
#PEro el clinete puede acutalizar nombre y o precio, por lo que no son forzosamente requeridos.ad

#Vamos a agregar el esquema plano de los tags

class PlainTagSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str()
    
    

class ItemUpdateSchema(Schema):
    name = fields.Str()
    #Name será un campo siempre requerido entre los datos de entrada.
    price =fields.Float()
    
    #Podemos agregar por último un id de tienda que puede ser ingresado o no por el usuario.
    #Se agregará en caso de querer actualizar un item, pero si el item no existe entonces lo crearemos
    store_id=fields.Int()
    
    
#Por último añadiremos nuestros esquemas para tienda y items más complejos que heredarán ciertas cosas de las clases anteriores.

class ItemSchema(PlainItemSchema):
    #Añadirá campos de tienda:
    store_id=fields.Int(required=True,load_only=True)
    #Es decir, cuando sea que utilicemos Item Schema recibiremos el id del cliente
    #También vamos a tener una tienda "anidada"
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    #Este último será utilizado únicamente cuando regresemos información al cliente.
    
    #Agregaremos ahora tags, ya que tenemos una relación de mcuhos a muchos que queremos que se vea reflejada también en el esquema
    tags=fields.List(fields.Nested(PlainTagSchema(),dump_only=True))
    
#De igual forma tendremos un esquema de tienda más complejo.

class StoreSchema(PlainStoreSchema):
    #Que contará con una lista de items
    items=fields.List(fields.Nested(PlainItemSchema()) , dump_only=True)
    #Es decir, solo la utilizaremos para entrega información al cliente.
    tags=fields.List(fields.Nested(PlainTagSchema()) , dump_only=True)
    
    
#Agregamso el esquema de tags, que en este caso será similar al de items

#YA que solo recibirá store id y nombre de tienda

class TagSchema(PlainTagSchema):
    #Añadirá campos de tienda:
    store_id=fields.Int(load_only=True)
    #Es decir, cuando sea que utilicemos Item Schema recibiremos el id del cliente
    #También vamos a tener una tienda "anidada"
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    
    #Añadimos los items para que se vea relfejada la relación muchos a muchos.
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    

#Ahora añadieremos una clase extra.

class TagAndItemSchema(Schema):
    message=fields.Str()
    item=fields.Nested(ItemSchema)
    tag=fields.Nested(TagSchema)


class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    #Recibiremos un ID del cliente
    
    #ASí como el usario y contraseña
    username=fields.Str(required=True)
    
    password=fields.Str(required=True,load_only=True)
    
    #load only
    """
    Nunca quieres regresar la contraseña al cliente, únicamente el usuario
    Esta restricción en la base de datos es fundamental
    Para que la infprmación de las contraseñas nunca quede expuesta al cliente
    
    """
    
    
    