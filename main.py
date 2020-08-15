# ----------------------------------------
# create fastapi app 
# ----------------------------------------
from fastapi import FastAPI
app = FastAPI()

# ----------------------------------------
# setup templates folder
# ----------------------------------------
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

# ----------------------------------------
# setup static files folder
# ----------------------------------------
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
# can use images as it is eg. <img src='static-img.jpg'>

# ----------------------------------------
# setup db
# ----------------------------------------
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine) #creates tables
# stocks db will appear once you run uvicorn.
# get into sqlite and try `.schema`


# ----------------------------------------
# import custom modules
# ----------------------------------------



# ----------------------------------------
# dependency injection
# ----------------------------------------
from fastapi import Depends

def get_db():
	""" returns db session """
	
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close


# ----------------------------------------
# bg tasks
# ----------------------------------------
from fastapi import BackgroundTasks

def fetch_real_time(pk: int):
	pass


# ----------------------------------------
# define structure for requests (Pydantic & more)
# ----------------------------------------
from fastapi import Request # for get
from pydantic import BaseModel # for post

class StockRequest(BaseModel):
	symbol: str
	
class CurPairRequest(BaseModel):
	cur_pair: str


# ----------------------------------------
# ----------------------------------------
# routes and related funcs
# ----------------------------------------
# ----------------------------------------
@app.get("/")
def api_home(request: Request):
	"""
	home page to display all real time values
	"""
	
	context = {
		"request": request
	}
	return templates.TemplateResponse("home.html", context)


@app.post("/api/curencypair")
async def add_currency_pairs(cur_pair_req: CurPairRequest,  background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
	"""
	adds given currecy pair TABLEs to db
	"""
		
	curPair = models.CurPairs()
	curPair.cur_pair = cur_pair_req.cur_pair
	db.add(curPair)
	db.commit()
		
	# in correct place
	background_tasks.add_task(fetch_real_time, curPair.id)
	
	return {"status": "ok"}
	
	
@app.delete("/api/curencypair")
def remove_currency_pair(cur_pair_req: CurPairRequest, db: Session = Depends(get_db)):
	"""
	Remove given curencypair TABLE from DB
	"""
	
	return None


@app.post("/api/stock")
async def add_stock(stock_req: StockRequest, background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
	"""
	adds given stock to db
	"""
	
	stock = models.Stocks()
	print(stock_req.symbol)
	stock.symbol = stock_req.symbol
	db.add(stock)
	db.commit()
		
	
	background_tasks.add_task(fetch_real_time, stock.id) 
	
	return None
	

@app.delete("/api/stock")
def remove_stock(stock_req: StockRequest, db: Session = Depends(get_db)):
	"""
	deletes given stock table from db
	"""
	
	return None



# ----------------------------------------
# end
# ----------------------------------------
