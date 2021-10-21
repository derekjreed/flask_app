#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import json
import dateutil.parser
import babel
import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from models import *


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/', methods=['GET'])
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  
  data = []
 
  state_and_city = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state)
  for x in state_and_city:
    venues = []
    venue_list = Venue.query.filter(Venue.state == x.state).filter(Venue.city == x.city).all()
    
    for y in venue_list:
      num_upcoming_shows = db.session.query(Show).filter(Show.venue_id == y.id).filter(Show.start_time > datetime.now()).count()
      venues.append({'id': y.id, 'name': y.name, 'num_upcoming_shows': num_upcoming_shows })
      
    data.append({'city': x.city, 'state': x.state, 'venues': venues})
    
  return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():

  search_term = request.form.get('search_term', '')
  result = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
  count = len(result)
  response = {"count": count, "data": result}


  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  
  past_shows=[]
  past_show_count=0
  shows_query_past =  db.session.query(Show).join(Artist).filter(Show.venue_id== venue_id).filter(Show.start_time<datetime.now()).all()
  for i in shows_query_past:
      past_shows.append({ "artist_id": i.artist.id, "artist_name": i.artist.name, "artist_image_link": i.artist.image_link, "start_time": str(i.start_time)})
      past_show_count += 1


  upcoming_shows = []
  upcoming_shows_count=0
  shows_query_future =  db.session.query(Show).join(Artist).filter(Show.venue_id== venue_id).filter(Show.start_time>datetime.now()).all()
  for i in shows_query_future:
      upcoming_shows.append({ "artist_id": i.artist.id, "artist_name": i.artist.name, "artist_image_link": i.artist.image_link, "start_time": str(i.start_time)})
      upcoming_shows_count += 1

  
  venue = Venue.query.filter(Venue.id == venue_id).first()
  
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": [venue.genres],
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,  
    "phone": venue.phone,
    "website_link": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,   
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_show_count,
    "upcoming_shows_count": upcoming_shows_count,
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  form = VenueForm(request.form)
  try:
    venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      website_link=form.website_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data        
    )

    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    print(e)
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed')
    db.session.rollback()
  finally:
    db.session.close()
  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  
  try:
   venue = Venue.query.get(venue_id)
   db.session.delete(venue)
   db.session.commit()
  except:
   db.session.rollback()
  finally:
   db.session.close()
  return jsonify({'success': True})



#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  data = []
  data = db.session.query(Artist.id, Artist.name).all()
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
 
  response = {}
  result = []
  search_term = request.form.get('search_term', '')
  search_result = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()
  count = len(search_result)
  for x in search_result:
    result.append({'id': x.id, 'name': x.name, 'num_upcoming_shows': '0'})
  response = {"count": count, "data": result}

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  past_shows=[]
  past_show_count=0
  #shows_query_past = db.session.query(Show).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()

  shows_query_past = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()
  for i in shows_query_past:
      past_shows.append({ "venue_id": i.venue.id, "venue_name": i.venue.name, "venue_image_link": i.venue.image_link, "start_time": str(i.start_time)})
      past_show_count += 1


  upcoming_shows = []
  upcoming_shows_count=0
  #shows_query_future = db.session.query(Show).filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()

  shows_query_future = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()
  for i in shows_query_future:
      upcoming_shows.append({ "venue_id": i.venue.id, "venue_name": i.venue.name, "venue_image_link": i.venue.image_link, "start_time": str(i.start_time)})
      upcoming_shows_count += 1



  artist = Artist.query.filter(Artist.id == artist_id).first()

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": [artist.genres],
    "city": artist.city,
    "state": artist.state,  
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "website_link" : artist.website_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,   
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_show_count,
    "upcoming_shows_count": upcoming_shows_count,
  } 
  print(data)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.filter(Artist.id == artist_id).first()
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  artist = Artist.query.filter(Artist.id == artist_id).first()
  try:

    artist.name=request.form['name']
    artist.city=request.form['city']
    artist.state=request.form['state']
    artist.phone=request.form['phone']
    artist.genres=request.form.getlist('genres')
    artist.image_link=request.form['image_link']
    artist.facebook_link=request.form['facebook_link']
    artist.website_link=request.form['website_link']
    # Get boolean back on checked = artist.seeking_talent in template
    artist.seeking_venue=bool(request.form.get('seeking_venue', False))
    artist.seeking_description=request.form['seeking_description'] 

    print(artist)
    print(artist.seeking_venue)
    db.session.add(artist)
    db.session.commit()
  except Exception as e:
    print(e)
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = Venue.query.filter(Venue.id == venue_id).first()
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  venue = Venue.query.filter(Venue.id == venue_id).first()
  try:

    venue.name=request.form['name']
    venue.city=request.form['city']
    venue.state=request.form['state']
    venue.address=request.form['address']
    venue.phone=request.form['phone']
    venue.genres=request.form['genres']
    venue.image_link=request.form['image_link']
    venue.facebook_link=request.form['facebook_link']
    venue.website_link=request.form['website_link']
    # Get boolean back on checked = venue.seeking_talent in template
    venue.seeking_talent=bool(request.form.get('seeking_talent', False))
    venue.seeking_description=request.form['seeking_description'] 

    print(venue)
    print(venue.seeking_talent)
    db.session.add(venue)
    db.session.commit()
  except Exception as e:
    print(e)
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  form = ArtistForm(request.form)
  try:
    artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      genres=form.genres.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      website_link=form.website_link.data,
      seeking_venue=form.seeking_venue.data,
      seeking_description=form.seeking_description.data     
    )
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except Exception as e:
    print(e)
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed')
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  all_shows = Show.query.all()
  data = []
  for show in all_shows:
      data.append({'venue_id' : show.venue.id, 'venue_name' : show.venue.name, 'artist_id' : show.artist.id, 'artist_name' : show.artist.name, 'artist_image_link' : show.artist.image_link, 'start_time' : format_datetime(str(show.start_time)) })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
 form = ShowForm(request.form)

 try:
  show = Show(
    artist_id=request.form['artist_id'],
    venue_id=request.form['venue_id'],
    start_time=request.form['start_time'],        
    )
  form.populate_obj(show)
  db.session.add(show)
  db.session.commit()
  # on successful db insert, flash success
  flash('Show was successfully listed!')

 except Exception as e:
    print(e)
    flash('An error occurred. Show ' + request.form['name'] + ' could not be listed')
    db.session.rollback()
 finally:
    db.session.close()
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port)