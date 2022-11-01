from db import db


class ItemsTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    #Un link a ITEMS (llave foranea)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    #Un link a TAGS (llave foranea)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    
    #Esta es la forma de definir una relación muchos a muchos.
    #Este modelo tendrá un ID propio que estará ligado a las muchas
    
     