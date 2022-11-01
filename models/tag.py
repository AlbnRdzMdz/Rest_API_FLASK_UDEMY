from db import db

class TagModel(db.Model):
    __tablename__="tags"
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    #El nombré será único, es decir, dos tags diferente no podrán tener el mismo nombre
    store_id= db.Column(db.Integer(),db.ForeignKey("stores.id"),nullable=False)
    
    store=db.relationship("StoreModel",back_populates="tags")
    
    items=db.relationship("ItemModel",back_populates="tags",secondary="items_tags")
    #Al hacer esto lo que estamos haciendo es el link con la tabla secundaria que nos dirá que items estaran relacionados con el tag ID
    
    

