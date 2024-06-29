import flask 
import db

app = flask.Flask(__name__)

""" 
- We need a table which represents the idea 
- We need a mood category table 

"""
# db.init()

@app.route("/")
def main():
    return flask.render_template("index.html")    

@app.route("/create", methods=["GET", "POST"])
def create_idea():
    if flask.request.method == "POST":
        content = flask.request.form
        print(content)
        return flask.redirect("/")
    else:
        return flask.render_template("create.html", items=["Freude", "Trauer"]) 

if __name__ == "__main__":
    app.run()
