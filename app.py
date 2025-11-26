from flask import Flask, render_template, request

import model

app = Flask(__name__)

@app.get("/")
def opening_page():
    data = model.get_log_data()
    return render_template(
        "pattern.html",
        the_title="Welcome to Xword on the Web!",
        data_table=data
    )

@app.get("/byorder/<what>")
def byorder(what):
    data = model.get_log_data(what)
    return render_template(
        "ordered.html",
        data_table=data
    )

@app.post("/processpattern")
def get_the_results():
    pat = request.form["pattern"]
    results = xword.find_possible_matches(pat)

    model.add_to_database(pat, len(results))

    return ", ".join(results)

if __name__ == "__main__":
    app.run(debug=True, port=5001)