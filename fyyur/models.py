from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
db = SQLAlchemy()

# TODO: connect to a local postgresql database
def setup_db(app):
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/todoapp'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

def get_upcoming_show_for_venue(venue_id):
    return db.session.query(Show).filter(
        Show.start_time > datetime.datetime.now(),
        Show.venue_id == venue_id
    ).all()

def get_past_show_for_venue(venue_id):
    return db.session.query(Show).filter(
                Show.start_time < datetime.datetime.now(),
                Show.venue_id == venue_id
            ).all()
        
def get_upcoming_show_for_artist(artist_id):
    return db.session.query(Show).filter(
            Show.start_time > datetime.datetime.now(),
            Show.artist_id == artist_id
    ).all()

def get_past_show_for_artist(artist_id):
    return db.session.query(Show).filter(
            Show.start_time < datetime.datetime.now(),
            Show.artist_id == artist_id
    ).all()

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    genres = Column(ARRAY(String))
    address = Column(String(120))
    city = Column(String(120))
    state = Column(String(120))
    phone = Column(String(120))
    website = Column(String(120))
    facebook_link = Column(String(120))
    seeking_talent = Column(Boolean,default=False)
    seeking_description = Column(String(500))
    image_link = Column(String(500))
    shows = db.relationship('Show', backref='Venue', lazy='dynamic', cascade="save-update, delete-orphan")

    def venue_search(self):
        upcoming_show = get_upcoming_show_for_venue(self.id)
        return {
            'name':self.name,
            'id':self.id,
            'upcoming_show_count': len(upcoming_show)
            }

    def get_data_dict(self):  
        upcoming_shows =  get_upcoming_show_for_venue(self.id) 
        past_shows = get_past_show_for_venue(self.id)
        return {
            'name':self.name,
            "id":self.id,
            "phone":self.phone,
            'city':self.city,
            'state':self.state,
            'address':self.address,
            'genres':self.genres,
            'image_link':self.image_link,
            'facebook_link':self.facebook_link,
            'seeking_description':self.seeking_description,
            'seeking_talent' :self.seeking_talent,
            'upcoming_shows' :[(show.get_dict_obj()) for show in upcoming_shows],
            'past_shows': [(show.get_dict_obj()) for show in past_shows],
            'past_shows_count' :len(past_shows),
            'upcoming_shows_count': len(upcoming_shows)
        }
      
    
class Artist(db.Model):
    __tablename__ = 'Artist'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    id = Column(Integer, primary_key=True)
    name = Column(String)
    genres = Column(ARRAY(String))
    city = Column(String(120))
    state = Column(String(120))
    phone = Column(String(120))
    website = Column(String(120))
    facebook_link = Column(String(120))
    seeking_venue = Column(Boolean,default=False)
    seeking_description = Column(String(500))
    image_link = Column(String(500),default='https://via.placeholder.com/3999')
    shows = db.relationship('Show', backref='Artist', lazy='dynamic', cascade="save-update, delete-orphan")

    def  artist_search_details(self):
        upcoming_shows =  get_upcoming_show_for_artist(self.id) 
        return {
            'name':self.name,
            "id":self.id,
            'upcoming_show_count': len(upcoming_shows)
        }

    def get_data_dict(self):  
        upcoming_shows =  get_upcoming_show_for_artist(self.id) 
        past_shows = get_past_show_for_artist(self.id)
        return {
            'name':self.name,
            "id":self.id,
            "phone":self.phone,
            'genres':self.genres,
            'seeking_venue' :self.seeking_venue,
            'seeking_description':self.seeking_venue,
            'website':self.website,
            'image_link':self.image_link,
            'facebook_link':self.facebook_link,
            'upcoming_shows': [ (show.get_dict_obj()) for show in upcoming_shows],
            'past_shows': [ (show.get_dict_obj()) for show in past_shows],
            'past_shows_count' :len(past_shows),
            'upcoming_shows_count': len(upcoming_shows)}
# TODO Implement Show models, and complete all model relationships and properties, as a database migration

class Show(db.Model):
    __tablename__ = 'Show'

    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('Venue.id'))
    artist_id = Column(Integer, ForeignKey('Artist.id'))
    start_time = Column(DateTime, nullable=False)

    def get_dict_obj(self):
        print("self",type(self.start_time))
        return {
                "venue_id": self.venue_id,
                "venue_name": self.Venue.name,
                "artist_id": self.artist_id,
                "artist_name": self.Artist.name,
                "artist_image_link": self.Artist.image_link,
                "start_time": self.start_time.strftime("%m/%d/%Y, %H:%M")
        }