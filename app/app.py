import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
        SELECT * FROM
            (SELECT COUNT(*) n_cathegory FROM CATHEGORY)
        JOIN
            (SELECT COUNT(*) n_company FROM COMPANY)
        JOIN
            (SELECT COUNT(*) n_developer FROM DEVELOPER)
        JOIN
            (SELECT COUNT(*) n_dlc FROM DLC)
        JOIN
            (SELECT COUNT(*) n_game FROM GAME)
        JOIN
            (SELECT COUNT(*) n_music FROM MUSIC)
        JOIN
            (SELECT COUNT(*) n_product FROM PRODUCT)
        JOIN
            (SELECT COUNT(*) n_publisher FROM PUBLISHER)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html', stats = stats)

 