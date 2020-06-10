#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
from datetime import *
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from models import setup_db, Venue, Artist, Show
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
db = setup_db(app)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = db.session.query(Venue).distinct(Venue.state,Venue.city).order_by('state','city').all()
  data=[]
  for v in venues:
    data.append({'city':v.city,'state':v.state})
  for d in data:
    d['venues'] = []
    # get all value based on state and city
    filter_by_city_state = db.session.query(Venue).filter_by(city= d['city'], state = d['state']).all()
    for venue in filter_by_city_state:
      venue_details = venue.get_data_dict()
      d['venues'].append(venue_details)
  
  return render_template('pages/venues.html', areas=data);

  
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_query = request.form.get('search_term')
  venues = db.session.query(Venue).filter(Venue.name.ilike('%'+search_query+'%')).all()
  count =len(venues)
  data=[]
  for venue in venues:
      venue_detail = venue.venue_search_details()
      data.append(venue_detail)
  response ={
          "count":count,
          "data":data
        }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = db.session.query(Venue).get(venue_id)
  if venue:
    data = venue.get_data_dict()
    
    return render_template('pages/show_venue.html', venue=data)
  else:
    return render_template('errors/404.html')

  
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  #print(request.form) 
  # getting form data 
  error = False
  try:
    formdata = request.form
    print(formdata)
    
    name = formdata.get('name')
    city = formdata.get('city')
    state = formdata.get('state')
    genres = formdata.getlist('genres')
    address = formdata.get('address')
    phone = formdata.get('phone')
    image_link = formdata.get('image_link')
    facebook_link  = formdata.get('facebook_link')
    website =formdata.get('website')
    seeking_talent = formdata.get('seeking_talent')
    if seeking_talent is None:
      seeking_talent = False
    else:
      seeking_talent = formdata.get('seeking_talent')
    seeking_description = formdata.get('seeking_description')

    venue = Venue(name=name,city = city,state = state,phone = phone, genres = genres, 
                 address = address, image_link = image_link, facebook_link = facebook_link,
                 website = website, seeking_talent = seeking_talent, seeking_description = seeking_description )
    db.session.add(venue)
    db.session.commit()    
  
  except :
    error=True
    db.session.rollback()
    print(sys.exc_info())

  finally:
    db.session.close()
  
  if  error:
    # display error message
    flash('An error occurred. Venue ' + name+ ' could not be listed.')
  else:
    
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  try:
    venue = db.session.query(Venue).get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = db.session.query(Artist).distinct(Artist.name).all()
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_query = request.form.get('search_term')
  artists = db.session.query(Artist).filter(Artist.name.ilike('%'+search_query+'%')).all()
  count =len(artists)
  data=[]
  for artist in artists:
      artist_detail = artist.artist_search_details()
      data.append(artist_detail)
  response ={
          "count":count,
          "data":data
        }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = db.session.query(Artist).get(artist_id)
  if artist:
    data = artist.get_data_dict()
    return render_template('pages/show_artist.html', artist=data)
  else:
    return render_template('errors/404.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  print(artist)
  if artist:
    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    return render_template('forms/edit_artist.html', form=form, artist=artist)
  else:
    return render_template('errors/404.html')

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  print("Artist_id",artist_id)
  try:
    print("editing Artist")
    error = False
    artist = db.session.query(Artist).get(artist_id)
    print(artist)
    formdata  = request.form
    artist.name = formdata.get('name')
    artist.city = formdata.get('city')
    artist.state = formdata.get('state')
    artist.genres = formdata.getlist('genres')
    artist.address = formdata.get('address')
    artist.phone = formdata.get('phone')
    artist.image_link = formdata.get('image_link')
    artist.facebook_link  = formdata.get('facebook_link')
    artist.website =formdata.get('website')
    seeking_venue = formdata.get('seeking_venue')
    if seeking_venue is None:
      artist.seeking_venue = False
    else:
      artist.seeking_venue = formdata.get('seeking_venue')
    artist.seeking_description = formdata.get('seeking_description')
    db.session.commit()
  except:
    err = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated')
  else:
    flash('Artist ' + request.form['name'] + ' was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))



@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = db.session.query(Venue).get(venue_id)
  print(venue)
  if venue:
    form.name.data = venue.name
    form.genres.data = venue.genres
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    return render_template('forms/edit_venue.html', form=form, venue=venue)

  else:
    return render_template('errors/404.html')
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    print("Editing venue")
    error = False
    venue = db.session.query(Venue).get(venue_id)
    print(venue)
    formdata  = request.form
    venue.name = formdata.get('name')

    venue.city = formdata.get('city')
    venue.state = formdata.get('state')
    venue.genres = formdata.getlist('genres')
    venue.address = formdata.get('address')
    venue.phone = formdata.get('phone')
    venue.image_link = formdata.get('image_link')
    venue.facebook_link  = formdata.get('facebook_link')
    venue.website =formdata.get('website')
    seeking_talent = formdata.get('seeking_talent')
    if seeking_talent is None:
      venue.seeking_talent = False
    else:
      venue.seeking_talent = formdata.get('seeking_talent')
    venue.seeking_description = formdata.get('seeking_description')
    db.session.commit()
  except:
    err = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if err:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error=False
  try:
    formdata = request.form
    print(formdata)
    name = formdata.get('name')
    city = formdata.get('city')
    state = formdata.get('state')
    genres = formdata.getlist('genres')
    
    phone = formdata.get('phone')
    image_link = formdata.get('image_link')
    facebook_link  = formdata.get('facebook_link')
    website =formdata.get('website')
    seeking_venue = formdata.get('seeking_venue')
    if seeking_venue is None:
      seeking_venue = False
    else:
      seeking_venue = formdata.get('seeking_venue')
    seeking_description = formdata.get('seeking_description')

    artist = Artist(name=name,city = city,genres = genres, state = state,phone = phone , 
                  image_link = image_link, facebook_link = facebook_link,
                  seeking_description  = seeking_description, seeking_venue = seeking_venue, website = website )
    db.session.add(artist)
    db.session.commit()    
  except :
    db.session.rollback()
    err=True
    # flash('An error occurred. Venue ' + name+ ' could not be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()

  
  if  error:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
  
  else:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  try:
    data = db.session.query(Show).all()
    d=[]
    for show in data:
      show_details={
        "venue_id": show.venue_id,
        "venue_name":show.Venue.name,
          # "venue_name": self.Venue.name,
        "artist_id": show.artist_id,
        "artist_name":show.Artist.name,
        "artist_image_link":show.Artist.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
      }
      d.append(show_details)

    
    return render_template('pages/shows.html', shows=d )
  except:
    print(sys.exc_info())
  finally:
    db.session.close()

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    error=False
    new_show = Show(
      venue_id=request.form['venue_id'],
      artist_id=request.form['artist_id'],
      start_time=request.form['start_time'],
    )
    db.session.add(new_show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    flash('Show was successfully listed!')
  
  return render_template('pages/home.html')
  
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
