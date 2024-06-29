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

@app.route("/")
def main(context: None | dict = None):
    if context is None: 
        context = {"message": None}
    conn = sqlite3.connect(constants.DATABASE_NAME)
    result = conn.cursor().execute("SELECT ideas.id, heading, content, name FROM ideas, category where fcategory=category.id").fetchall()
    context["ideas"] = result
    return flask.render_template("index.html", context=context)    

@app.route("/create", methods=["GET", "POST"])
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

if __name__ == "__main__":
    app.run()
