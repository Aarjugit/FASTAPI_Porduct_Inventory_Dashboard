#import FastAPI class from fastapi library
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import product
from database import session,engine
import database_models
from sqlalchemy.orm import Session
#done making fastapi object
app = FastAPI()
app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:3000"],
   allow_methods=["*"]
)
database_models.Base.metadata.create_all(bind=engine)
#we will use decorators alongwith http method get 
@app.get("/")
def greet():
    return "Welcome to Aarju's Tracker"

products = [
    product(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    product(id=2, name="Smartphone", description="A latest model smartphone", price=699.99, quantity=25),
    product(id=3, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=15),
    product(id=4, name="Monitor", description="4K UHD Monitor", price=399.99, quantity=8),
]

def get_db():
   db=session()
   try:
      yield db
   finally:
      db.close() 
#we need to add data into db which is given inside products
def init_db():
   db=session()
   count = db.query(database_models.product).count
   if count == 0:
      
      for product in products:
        db.add(database_models.product(**product.model_dump()))

      db.commit()
       
init_db()

# ------GET/READ----------
@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
   
    db_products = db.query(database_models.product).all()
    #query
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int, db:Session = Depends(get_db)):
   db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
   if db_product:
      return db_product
      
    
   return "product not found"
    
# ------POST/ADD----------  
@app.post("/products")
def add_product(product: product, db: Session = Depends(get_db)):
   db.add(database_models.product(**product.model_dump()))
   db.commit()
   return product

#---------PUT/UPDATE--------
@app.put("/products/{id}")
def update_product(id:int, product: product, db: Session = Depends(get_db)):
   db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
   if db_product:
      db_product.name = product.name
      db_product.description = product.description
      db_product.price = product.price
      db_product.quantity = product.quantity
      db.commit()
      return "Product Updated Successfully"
   else:
      return "Product Not Found"
   # for i in range(len(products)):
   #      if products[i].id == id:
   #         products[i] = product
   #         return "Product Added Successfully"
   #      return "Product Not Found"
#--------DELETE/REMOVE--------    
@app.delete("/products/{id}")
def delete_product(id: int , db: Session = Depends(get_db)):
   db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
   if db_product:
      db.delete(db_product)
      db.commit()
      return "Product Deleted Successfully"
   else:
      return "Product Not Found"
   # for i in range(len(products)):
   #    if products[i].id == id:
   #       del products[i]
   #       return "Product Deleted Successfully" 
   #    return "Product Not Found"