from flask import Flask, render_template, request

import model

app = Flask(__name__)

@app.get("/")
@app.get("/rules")
def opening_page():
    return render_template(
        "home.html",
        the_title="Welcome to Word Game 4 on the Web!",
    )

@app.get("/startgame")
def game():
    sourceword = ""

    return render_template(
        "game.html",
        the_title="Let's get busy!",
        the_sourceword=sourceword
    )

@app.get("/top10")
def leaderboard():
    data = model.get_leaderboard_data()
    return render_template(
        "leaderboard.html",
        the_title="The top ten scores",
        data_table=data
    )

@app.post("/processwords")
def get_the_results():
    ans = request.form["answer"]
    results = []
    time = 0.0

    if not results:
        return render_template(
            "win.html",
            the_title="You're a winner!",
            the_time=time,
            the_ans=ans
        )
    else:
        return render_template(
            "lose.html",
            the_title="Better luck next time.",
            the_results=results
        )

@app.post("/processhighscore")
def record_high_score():
    name = request.form["username"]
    data = model.get_leaderboard_data()
    position = 0
    players = 0

    return render_template(
        "postwin.html",
        the_title="How did you do?",
        the_position=position,
        the_players=players,
        data_table=data
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)