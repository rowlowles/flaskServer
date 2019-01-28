from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

import json

secrets = json.load(open('secrets.json', encoding="utf8"))

db = secrets['db']
user = secrets['user']
port = secrets['port']
host = secrets['host']
password = secrets['password']

engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+db)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

def init_db():
    metadata.create_all(bind=engine)