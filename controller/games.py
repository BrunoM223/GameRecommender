from flask import Blueprint as bt, render_template, request as rq, session, redirect, url_for
from models.games import Game
from models.ratings import Rating
from models.decorators import needs_login
from models.user import User
from common.recommend import Recommend
from urllib.parse import quote


games_blueprint = bt('games', __name__)
recommend = Recommend()


@games_blueprint.route('/')
def index():
    games = Game.find_random(10)
    return render_template('games/index.html', games=games)


@games_blueprint.route('/<asin>', methods=['GET', 'POST'])
@needs_login
def game(asin):
    this_game = Game.find_by_asin(asin)
    user = User.find_by_username(session['username'])
    average = Rating.avg_ratings_for_game(asin)
    rating = Rating.ratings_for_user(user.reviewerID, getattr(this_game, 'asin'))

    if rq.method == 'POST':
        rating = int(rq.form.get('select'))
        Rating(user.reviewerID, this_game.asin, '', '', rating).save_to_mongo()
        return render_template('games/game.html', rated=True, game=this_game, average=average, rating=rating)
    else:
        if rating != 0 and rating is not None and rating != '':
            return render_template('games/game.html', rated=True, game=this_game, average=average, rating=rating)
        else:
            return render_template('games/game.html', rated=False, game=this_game, average=average)


@games_blueprint.route('/rated')
@needs_login
def rated():
    games = []
    user = User.find_by_username(session['username'])
    ratings = Rating.all_ratings_for_user(user.reviewerID)
    has_ratings = False
    if len(ratings) > 0:
        has_ratings = True
        for rating in ratings:
            game = Game.find_by_asin(rating.asin)
            games.append(game)
    return render_template('games/rated.html', games=games, rated=has_ratings)


@games_blueprint.route('/recommended')
@needs_login
def recommended_games():
    user = User.find_by_username(session['username'])
    ratings = Rating.all_ratings_for_user(user.reviewerID)
    if len(ratings) >= 5:
        games_recommended = recommend.recommend_user(user.reviewerID)
        return render_template('games/recommended.html', games=games_recommended, rated=True, not_liked=False)
    else:
        return render_template('games/recommended.html', rated=False)


@games_blueprint.route('/notrecommended')
@needs_login
def not_recommended_games():
    user = User.find_by_username(session['username'])
    ratings = Rating.all_ratings_for_user(user.reviewerID)
    if len(ratings) >= 5:
        games_recommended = recommend.recommend_user(user.reviewerID, not_liked=True)
        return render_template('games/recommended.html', games=games_recommended, rated=True, not_liked=True)
    else:
        return render_template('games/recommended.html', rated=False)


@games_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    if rq.method == 'POST':
        if 'Search' in rq.form and rq.form['Search'] != "":
            return redirect(url_for('games.search', search=rq.form['Search']))
    if 'search' in rq.args:
        games = Game.find_by_text(rq.args['search'])
        return render_template('games/search.html', games=games, found=True)

    return render_template('games/search.html')