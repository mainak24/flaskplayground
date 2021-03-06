#
# flplay4c.py  - cleaned version of flplay4b.py
#
# declarative reflect with derived/calculated/grafted column - hybrid_property - works. 2016-02-10. David Gleba

'''
This is declarative reflect from these web pages..

See declarative on this page...
    http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/
=
reflect..
    http://stackoverflow.com/questions/6290162/how-to-automatically-reflect-database-to-sqlalchemy-declarative
        works 2016-02-11
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask_admin.contrib import sqla

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String

from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '1234567901asdfafafaee'

# create connection with 'reflect' [read table columns] of the database
engine = create_engine('sqlite:///test.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
meta = MetaData(bind=engine)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# reflect users table..

class User(Base):
    __table__ = Table('users', meta, autoload=True)
    
    # create derived/calculated/grafted column..      
    @hybrid_property
    def ref1(self):
        return self.name + " " + self.email
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# enhance models...

class dgcUserAdmin(sqla.ModelView):
    column_display_pk = True
    column_list = ['id', 'name', 'email', 'ref1' ]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
# Create admin
admin = admin.Admin(app, name='db-4-reflect', template_mode='bootstrap3')
admin.add_view(dgcUserAdmin(User, db_session))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# utilities..

#initialize db..
def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    #import yourapplication.models
    Base.metadata.create_all(bind=engine)
    
# note this syntax.. #from yourapplication.database import db_session

# turn off session upon program exit.
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':

    # Create DB
    #db.create_all()
    
    #from yourapplication.database import init_db
    init_db()

    '''
    u = User('admin', 'admin@localhost')
    db_session.add(u)
    db_session.commit()
    '''
    
    # Start app
    app.run(host='0.0.0.0', port=5000, debug=True)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
