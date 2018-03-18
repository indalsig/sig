from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import settings

# connection_string = 'mysql+mysqldb://' + settings.MYSQL_USER + ':' + settings.MYSQL_PASSWD + '@' + \
#                     settings.MYSQL_HOST + '/' + settings.MYSQL_DBNAME + '?charset=utf8'

connection_string = 'postgresql+psycopg2://' + settings.PG_USER + ':' + settings.PG_PASSWD + '@' + \
                    settings.PG_HOST + '/' + settings.PG_DBNAME
engine = create_engine(connection_string)

Session = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()
