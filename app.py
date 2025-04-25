from flask import Flask, render_template, request, redirect, session
from gobblers import Gobbler

app = Flask(__name__, template_folder="templates")
# I don't know what the heck this does
app.secret_key = "secret123"  # Needed for session

def get_game():
    if 'game' not in session:
        session['game'] = Gobbler().__dict__
    game = Gobbler()
    game.__dict__.update(session['game'])
    return game

@app.route("/", methods=["GET", "POST"])
def index():
    game = get_game()

    if request.method == "POST":
        if not game.check_game_over():
            # communicate the size and the color
            position = tuple(request.form["move"])
            position = (int(position[0]), int(position[1]))
            size = int(request.form["size"])
            move = ((game.get_current_player(), size), position)
            game.make_move(move)
            session['game'] = game.__dict__

    return render_template("index.html", board=game.board, winner=game.check_game_over())

@app.route("/reset")
def reset():
    session.pop('game', None)
    return redirect("/")