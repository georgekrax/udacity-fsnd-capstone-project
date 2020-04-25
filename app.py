import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Actor, Movie, Performance

ROWS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  db_drop_and_create_all()

  CORS(app)
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response


  def paginate_results(request, selection):
    page = request.args.get('page', 1, type=int)
    
    start =  (page - 1) * ROWS_PER_PAGE
    end = start + ROWS_PER_PAGE

    objects = [object.format for object in selection]
    return objects[start:end]


  #----------------------------------------------------------------------------#
  # Endpoint /actors GET/POST/DELETE/PATCH
  #----------------------------------------------------------------------------#

  @app.route('/actors')
  @requires_auth('read:actors')
  def get_actors(payload):
    actors = Actor.query.all()
    actors_paginated = paginate_results(request, actors)

    if len(actors_paginated) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'actors': actors_paginated
    })

  @app.route('/actors', methods=['POST'])
  @requires_auth('create:actors')
  def insert_actors(payload):
    body = request.get_json()

    if not body:
          abort(400)

    name = body.get('name', None)
    age = body.get('age', None)

    gender = body.get('gender', 'Other')

    if not name or not age:
      abort(422)

    new_actor = (Actor(name = name, age = age, gender = gender))
    new_actor.insert()

    return jsonify({
      'success': True,
      'created': new_actor.id
    })

  @app.route('/actors/<actor_id>', methods=['PATCH'])
  @requires_auth('edit:actors')
  def edit_actors(payload, actor_id):
    body = request.get_json()

    if not actor_id or not body:
      abort(400)

    actor_to_update = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if not actor_to_update:
      abort(404)
    
    name = body.get('name', actor_to_update.name)
    age = body.get('age', actor_to_update.age)
    gender = body.get('gender', actor_to_update.gender)

    actor_to_update.name = name
    actor_to_update.age = age
    actor_to_update.gender = gender

    actor_to_update.update()

    return jsonify({
      'success': True,
      'updated': actor_to_update.id,
      'actor' : [actor_to_update.format]
    })

  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(payload, actor_id):
    if not actor_id:
      abort(400)
  
    actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if not actor_to_delete:
        abort(404)
    
    actor_to_delete.delete()
    
    return jsonify({
      'success': True,
      'deleted': actor_id
    })

  #----------------------------------------------------------------------------#
  # Endpoint /movies GET/POST/DELETE/PATCH
  #----------------------------------------------------------------------------#

  @app.route('/movies', methods=['GET'])
  @requires_auth('read:movies')
  def get_movies(payload):
    movies = Movie.query.all()
    movies_paginated = paginate_results(request, movies)

    if len(movies_paginated) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'movies': movies_paginated
    })

  @app.route('/movies', methods=['POST'])
  @requires_auth('create:movies')
  def insert_movies(payload):
    body = request.get_json()

    if not body:
          abort(400)

    title = body.get('title', None)
    release_date = body.get('release_date', None)

    if not title or not release_date:
      abort(422)

    new_movie = (Movie(title = title, release_date = release_date))
    new_movie.insert()

    return jsonify({
      'success': True,
      'created': new_movie.id
    })

  @app.route('/movies/<movie_id>', methods=['PATCH'])
  @requires_auth('edit:movies')
  def edit_movies(payload, movie_id):
    body = request.get_json()

    if not movie_id or not body:
      abort(400)

    movie_to_update = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if not movie_to_update:
      abort(404)

    title = body.get('title', movie_to_update.title)
    release_date = body.get('release_date', movie_to_update.release_date)

    movie_to_update.title = title
    movie_to_update.release_date = release_date

    movie_to_update.update()

    return jsonify({
      'success': True,
      'edited': movie_to_update.id,
      'movie' : [movie_to_update.format]
    })

  @app.route('/movies/<movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(payload, movie_id):
    if not movie_id:
      abort(400)
  
    movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if not movie_to_delete:
        abort(404)
    
    movie_to_delete.delete()
    
    return jsonify({
      'success': True,
      'deleted': movie_id
    })

  #----------------------------------------------------------------------------#
  # Error Handlers
  #----------------------------------------------------------------------------#
  @app.errorhandler(500)
  def unprocessable(error):
      return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal server error"
        }), 500

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable entity"
        }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
        }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
      return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(AuthError)
  def authentification_failed(AuthError): 
      return jsonify({
        "success": False, 
        "error": AuthError.status_code,
        "message": AuthError.error['description']
        }), AuthError.status_code


  return app

app = create_app()

if __name__ == '__main__':
    app.run(port=8080, debug=True)