from fastapi import FastAPI,Depends
import database_models
from models import Product
from database import session,engine
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


app = FastAPI()  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],)

database_models.Base.metadata.create_all(bind=engine)

products=[
    Product(id=1,name='iphone 13 pro',description='this is so far the latest iphone we have produced',price=60.4,quantity=20),
    Product(id=2,name='iphone 11',description='this phone is really good',price=67.4,quantity=20),
    Product(id=3,name='google poxel 13 pro',description='looking fressh',price=7.0,quantity=45),
    Product(id=4,name='infinix hot ',description='This is one of the best so far the latest iphone we have produced',price=76,quantity=23),
    Product(id=5,name='techno camon 11',description='very slimm and fast',price=34.4,quantity=66),
    Product(id=6,name='techno',description='try this you will thank me later',price=5.4,quantity=6),
    Product(id=7,name='itel pro',description='i cannot say anything about this one ',price=44.69,quantity=12),
    Product(id=8,name='iphone 4 max',description='cheap and very affordable yet swaggerific',price=4.23,quantity=25)
    
] 

def get_db():
    db=session()
    try:
        yield db

    finally:
        db.close()

def init_db():
    db=Session()
    count=db.query(database_models.Product).count
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()



#getting all the products
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
   db_products=db.query(database_models.Product).all()
   return db_products



#getting the product by id
@app.get("/products/{id}")
def get_product_by_id(id: int,db: Session = Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    return "product not found"


#creating a new product
@app.post("/products")
def create_product(product: Product,db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()

    return product
#update
@app.put("/products/{id}")
def update_product(id:int,product:Product,db: Session = Depends(get_db)):
     db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
     if db_product:
         db_product.name= product.name
         db_product.description= product.description
         db_product.price=product.price
         db_product.quantity=product.quantity
         db.commit()
         return "product Updated succesfully"
     else:
         return "No product found"
         

#delete
@app.delete("/products/{id}")
def delete_product(id:int,db: Session = Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Deleted succesfully"
    return "product not found"