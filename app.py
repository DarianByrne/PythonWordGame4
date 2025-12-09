# Darian Byrne
# C00296036
# 09/12/2025

from flask import Flask, render_template, request, session, redirect

from decimal import Decimal
import time
import model
import wordgame4

app = Flask(__name__)
app.secret_key = "fiftieth-monetary-both-rejoin-strained-stimuli-punctual-rearview-embattled-stretch-unroasted-treat-amuck-lather-unpaved-fidgety"

@app.get("/")
@app.get("/rules")
def opening_page():
    return render_template(
        "home.html",
        the_title="Welcome to Word Game 4 on the Web!",
    )

@app.get("/startgame")
def game():
    sourceword = wordgame4.pick_sourceword()
    session["sourceword"] = sourceword
    session["starttime"] = time.time()

    return render_template(
        "game.html",
        the_title="Let's get busy!",
        the_sourceword=sourceword
    )

@app.get("/top10")
def leaderboard():
    data = model.get_leaderboard_data(limit_10=True)
    return render_template(
        "leaderboard.html",
        the_title="The top ten scores",
        data_table=data
    )

@app.post("/processwords")
def get_the_results():
    ans = request.form["answer"]
    session["ans"] = ans
    sourceword = session["sourceword"]
    results = wordgame4.is_valid(sourceword, ans)
    starttime = session["starttime"]
    endtime = time.time()
    length = endtime - starttime
    t = Decimal(length).quantize(Decimal('.01'))
    session["length"] = length

    if not results:
        return render_template(
            "win.html",
            the_title="You're a winner!",
            the_time=t,
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
    # this code can be used to stop the user from recording themselves into the database multiple times
    # it is commented out because it's not part of the spec
    # uses get method as recorded may not be set, defaults to False
    # if session.get("recorded", False):
    #     return redirect("/")
    who = request.form["username"]
    sourceword = session["sourceword"]
    length = session["length"]
    ans = session["ans"].split(" ")
    matches = ", ".join(ans)
    model.add_to_database(length, who, sourceword, matches)
    # session["recorded"] = True
    data = model.get_leaderboard_data(limit_10=False)

    t = Decimal(length).quantize(Decimal('.01'))
    # https://www.geeksforgeeks.org/python/python-find-the-tuples-containing-the-given-element-from-a-list-of-tuples/
    position = [tup for tup in data if who in tup and t in tup][0][0]
    players = len(data)

    return render_template(
        "postwin.html",
        the_title="How did you do?",
        the_position=position,
        the_players=players,
        data_table=data[:10]
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)