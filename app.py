from flask import Flask, render_template as rt, url_for
from controller.games import games_blueprint
from controller.users import user_blueprint
import string
import random

random_str = "".join(random.choice(string.ascii_letters) for i in range(64))
app = Flask(__name__)
app.config['TESTING'] = True
app.secret_key = random_str
app.register_blueprint(games_blueprint, url_prefix='/games')
app.register_blueprint(user_blueprint, url_prefix='/users')


for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint} : {rule.rule}")


@app.route('/')
def home():
    return rt("home.html")


if __name__ == '__main__':
    app.run(debug=True)
