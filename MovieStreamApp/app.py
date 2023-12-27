import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
      (SELECT COUNT(*) n_movies FROM MOVIE)
    JOIN
      (SELECT COUNT(*) n_actors FROM ACTOR)
    JOIN
      (SELECT COUNT(*) n_genres FROM MOVIE_GENRE)
    JOIN 
      (SELECT COUNT(*) n_streams FROM STREAM)
    JOIN 
      (SELECT COUNT(*) n_customers FROM CUSTOMER)
    JOIN 
      (SELECT COUNT(*) n_countries FROM COUNTRY)
    JOIN 
      (SELECT COUNT(*) n_regions FROM REGION)
    JOIN 
      (SELECT COUNT(*) n_staff FROM STAFF)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html',stats=stats)

#Products
@APP.route('/products')
def list_products():
   products = db.execute('''
        SELECT *
        FROM products
        ORDER BY name
        ''')

# Games
@APP.route('/games/')
def list_games():
    games = db.execute('''
        SELECT product_id, game_id, kind_id, name, required_age, achievements, release_date, coming_soon, price, review_score, total_positive, total_positive, rating, owners, average_forever, median_forever, tags, sported_audio, categories, genres, platforms, packages, supported_lang
        FROM game
        NATURAL JOIN product
        ORDER BY name
    ''').fetchall()
    return render_template('game-list.html', games=games)


@APP.route('/games/<int:id>/')
def get_game(id):
    game = db.execute('''
        SELECT *
        FROM game
        NATURAL JOIN product
        WHERE product_id = ?     
    ''', [id]).fetchone()
    
    if game is None:
        abort(404, 'Game id {} does not exist.'.format(id))
        
    publishers_id = db.execute('''
        SELECT publishers_id
        FROM game
        NATURAL JOIN product
        WHERE product_id = ?
    ''', [id]).fetchone()
    
    publishers = {}
    for publisher in publishers_id:
        publishers[publisher] = db.execute('''
            SELECT name
            FROM company
            WHERE company_id = ?
        ''', [publisher]).fetchone()
    
    developers_id = db.execute('''
        SELECT developers_id
        FROM game
        NATURAL JOIN product
        WHERE product_id = ?
    ''', [id]).fetchone()
    
    developers = {}
    for developer in developers_id:
        developers[developer] = db.execute('''
            SELECT name
            FROM company
            WHERE company_id = ?
        ''', [developer]).fetchone()
    
    return render_template('game.html', game = game, publishers = publishers, developers = developers)


#DLCs
@APP.route('/dlcs/')
def list_dlcs():
    dlcs = db.execute('''
        SELECT *
        FROM dlc
        NATURAL JOIN product
        ORDER BY name
    ''').fetchall()
    return render_template('dlc-list.html', dlcs=dlcs)


@APP.route('/dlcs/<int:id>/')
def get_dlc(id):
    dlc = db.execute('''
        SELECT *
        FROM dlc
        NATURAL JOIN product
        WHERE product_id = ?     
    ''', [id]).fetchone()
    
    if dlc is None:
        abort(404, 'Dlc id {} does not exist.'.format(id))
        
    publishers_id = db.execute('''
        SELECT publishers_id
        FROM dlc
        NATURAL JOIN product
        WHERE product_id = ?
    ''', [id]).fetchone()
    
    publishers = {}
    for publisher in publishers_id:
        publishers[publisher] = db.execute('''
            SELECT name
            FROM company
            WHERE company_id = ?
        ''', [publisher]).fetchone()
    
    developers_id = db.execute('''
        SELECT developers_id
        FROM dlc
        NATURAL JOIN product
        WHERE product_id = ?
    ''', [id]).fetchone()
    
    developers = {}
    for developer in developers_id:
        developers[developer] = db.execute('''
            SELECT name
            FROM company
            WHERE company_id = ?
        ''', [developer]).fetchone()
    
    return render_template('dlc.html', dlc = dlc, publishers = publishers, developers = developers)

# Genres
@APP.route('/genres/')
def list_genres():
    genres = db.execute('''
      SELECT GenreId, Label 
      FROM GENRE
      ORDER BY Label
    ''').fetchall()
    return render_template('genre-list.html', genres=genres)

@APP.route('/genres/<int:id>/')
def view_movies_by_genre(id):
  genre = db.execute(
    '''
    SELECT GenreId, Label
    FROM GENRE 
    WHERE GenreId = ?
    ''', [id]).fetchone()

  if genre is None:
     abort(404, 'Genre id {} does not exist.'.format(id))

  movies = db.execute(
    '''
    SELECT MovieId, Title
    FROM MOVIE NATURAL JOIN MOVIE_GENRE
    WHERE GenreId = ?
    ORDER BY Title
    ''', [id]).fetchall()

  return render_template('genre.html', 
           genre=genre, movies=movies)

# Streams
@APP.route('/streams/<int:id>/')
def get_stream(id):
  stream = db.execute(
      '''
      SELECT StreamId, StreamDate, Charge, MovieId, Title, CustomerId, Name
      FROM STREAM NATURAL JOIN MOVIE NATURAL JOIN CUSTOMER 
      WHERE StreamId = ?
      ''', [id]).fetchone()

  if stream is None:
     abort(404, 'Stream id {} does not exist.'.format(id))

  return render_template('stream.html', stream=stream)


# Staff
@APP.route('/staff/')
def list_staff():
    staff = db.execute('''
      SELECT S1.StaffId AS StaffId, 
             S1.Name AS Name,
             S1.Job AS Job, 
             S1.Supervisor AS Supervisor,
             S2.Name AS SupervisorName
      FROM STAFF S1 LEFT JOIN STAFF S2 ON(S1.Supervisor = S2.StaffId)
      ORDER BY S1.Name
    ''').fetchall()
    return render_template('staff-list.html', staff=staff)

@APP.route('/staff/<int:id>/')
def show_staff(id):
  staff = db.execute(
    '''
    SELECT StaffId, Name, Supervisor, Job
    FROM STAFF
    WHERE staffId = ?
    ''', [id]).fetchone()

  if staff is None:
     abort(404, 'Staff id {} does not exist.'.format(id))
  superv={}
  if not (staff['Supervisor'] is None):
    superv = db.execute(
      '''
      SELECT Name
      FROM staff
      WHERE staffId = ?
      ''', [staff['Supervisor']]).fetchone()
  supervisees = []
  supervisees = db.execute(
    '''
      SELECT StaffId, Name from staff
      where Supervisor = ?
      ORDER BY Name
    ''',[id]).fetchall()

  return render_template('staff.html', 
           staff=staff, superv=superv, supervisees=supervisees)

