from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


engine=create_engine('postgresql://postgres:Bhavya3#8&!@localhost:5432/pizaaDB',
    echo=True
)

Base=declarative_base()

Session=sessionmaker()