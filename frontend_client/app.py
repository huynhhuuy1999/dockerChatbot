from flask import Flask, render_template, request, redirect, url_for, session
from neo4j import GraphDatabase

app = Flask(__name__, static_folder="public", static_url_path="/public")
app.secret_key = "1234"
driver = GraphDatabase.driver(
    "neo4j://localhost:7687", auth=("neo4j", "123456789"), database="test"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quanly")
def quanly():

    with driver.session() as neo4j_session:
        result = neo4j_session.run("Match(i:Intent) return i.name,i.text")
        data = [(record[0], record[1]) for record in result]
    return render_template("quanly.html", data=data)


if __name__ == "__main__":
    app.run(debug=True, port=8282, host="0.0.0.0")
