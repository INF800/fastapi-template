import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime
#from sqlalchemy.orm import relationship
from database import Base

class CurPairs(Base):
	"""
	Stores list of all cur pair table names that
	should be displayed in real time
	"""
	
	__tablename__ = "CurPairs"
	
	id         = Column(Integer, primary_key=True, index=True)
	time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
	cur_pair   = Column(String, index=True)
	price      = Column(String)
	change					= Column(String)
	per_change = Column(String)