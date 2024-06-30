import flask 
import sqlite3 
import constants
import logging

app = flask.Flask(__name__)
logger = logging.getLogger(__name__)

get_category = "SELECT * FROM category WHERE name=?"

def fetch_one(conn, sql, params): 
    cur = conn.cursor().execute(sql, params)
    return cur.fetchone()

def query_ideas(filter: dict):
    print(type(filter))
    conn = sqlite3.connect(constants.DATABASE_NAME)
    sql = "SELECT ideas.id, heading, content, name FROM ideas, category where fcategory=category.id"
    parameters = []
    for key in filter.keys():
        sql += f" AND {key}=?"
        parameters.append(filter[key])
    result = conn.cursor().execute(sql, tuple(parameters)).fetchall()
    return result

@app.route("/")
def main(context: None | dict = None):
    if context is None: 
        context = {"message": None}
    context["ideas"] = query_ideas(dict())
    return flask.render_template("index.html", context=context)    

@app.route("/create/", methods=["GET", "POST"])
def create_idea():
    if flask.request.method == "POST":
        content = flask.request.form
        category, heading, content = (content.get("category").strip(), content.get("title"), content.get("text"))
        conn = sqlite3.connect(constants.DATABASE_NAME)
        if not category.isalpha():
            return flask.render_template("error.html", error="Invalid category")
        cat = fetch_one(conn, get_category, (category,))
        if cat is None:
            conn.cursor().execute("INSERT INTO category(name) VALUES(?)", (category,))
            conn.commit()
            logger.info(f"Category {category} was created!")
        cat = fetch_one(conn, get_category, (category,))
        id = cat[0]
        conn.cursor().execute("INSERT INTO ideas(heading, content, fcategory) VALUES(?,?,?)", (heading, content, id,))
        conn.commit()
        conn.close(); 
        return main({"message": "Created new idea"})
    else:
        return flask.render_template("create.html", items=["Freude", "Trauer"]) 

@app.route("/search/", methods=["GET"])
def search():
    if flask.request.method == "GET":
        parts = {item[0]:item[1] for item in [i.split("=") for i in flask.request.query_string.decode().split("&")]}
        category = parts["search"]
        results = query_ideas({"category.name": category})
        if len(results) == 0:
            return flask.render_template("search.html", context={"message": "No results for this category!"})
        else:
            return flask.render_template("search.html", context={"ideas": results, "message": None})
    else:
        return flask.render_template("error.html", error="Method not allowed!") 

if __name__ == "__main__":
    app.run()
